import PyPDF2
import os
import re
import textwrap
import exemel_utils
import pdf_parse
from pathlib import Path


def main():

    pdfFiles = []
    # for each pdf in the 'Orders' folder, add the filenames to a list pdfFiles.
    orders_path_string = str(Path("./Orders/"))
    for filename in os.listdir(orders_path_string):
        if filename.endswith('.pdf'):
            file_path = os.path.join("Orders",filename)
            pdfFiles.append(file_path)

    pdfFiles.sort(key=str.lower)  # sorted in alphabetical order


    order_objs = {}
    num_of_orders = 0


    for file in pdfFiles:  # for each order pdf in the 'Orders' folder, create a pdf object and read the pdf.
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        num_of_orders += 1
        order_objs['Order {}'.format(num_of_orders)] = pdf_parse.Order(file,pdfReader) # Order class constructor

        current_order = order_objs['Order {}'.format(num_of_orders)] # stores the current order in the loop to a variable
        page_one_text = current_order.get_page_text()['Page 1']

        call_letters = pdf_parse.Order.get_call_letters(page_one_text)
        market_name = pdf_parse.Order.get_market_name(page_one_text)
        est_num = pdf_parse.Order.get_est_num(page_one_text)
        product_name = pdf_parse.Order.get_product_name(page_one_text)
        buyer_name = pdf_parse.Order.get_buyer_name(page_one_text)




        page_objs = {}

        for page_num, text in current_order.get_page_text().items(): # for each page in the order, create a page object
            page_objs['{}-{}'.format(current_order,page_num)] = pdf_parse.Page(page_num, text, call_letters) # Page class constructor
            current_page = page_objs['{}-{}'.format(current_order,page_num)]



            if current_page.page_with_spots() == True: # if the current page contains a schedule with spots, then read it.
                air_weeks = current_page.get_air_weeks()
                hiatus_weeks = current_page.get_hiatus_weeks(air_weeks)



                # for each line, create a line object
                line_objs = {}

                flight_end_date = pdf_parse.Page.get_flight_end_date(air_weeks)
                exemel_utils.endDate = exemel_utils.get_endDate(air_weeks)
                exemel_utils.startDate = exemel_utils.get_startDate(air_weeks)

                # For Debugging only

                # print(current_page.get_daypart_symbols())
                # print(current_page.get_spot_rates())
                # print(current_page.get_spot_durs())
                print(current_page.get_daypart_programs())

                #print(current_page.text)


                b = 0

                for i in current_page.get_line_nums(): # for each line on the page,
                    line_num = current_page.get_line_nums()[b]
                    daypart_program = current_page.get_daypart_programs()[b]
                    daypart_symbol = current_page.get_daypart_symbols()[b]
                    spot_rate = current_page.get_spot_rates()[b]
                    spot_dur = current_page.get_spot_durs()[b]
                    spot_count = current_page.get_spot_counts()[b]
                    daypart_note = current_page.get_daypart_notes()[b]
                    line_objs["{}-{}-Line {}".format(current_order.__str__(),current_page.__str__(),i)] = pdf_parse.Line(line_num, daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note, page_num, text, call_letters)
                    current_line = "{}-{}-Line {}".format(current_order.__str__(),current_page.__str__(),i)

                    b += 1
                    exemel_utils.create_xml_proposal_line(line_objs[current_line],air_weeks,hiatus_weeks,market_name,file)

        print("\nOrder #{}: {}".format(num_of_orders, current_order))
        print("Market Name: {}".format(market_name))
        print("Call Letters: {}".format(call_letters))
        print("Estimate Number: {}".format(est_num))
        print("Product: {}".format(product_name))
        print("Buyer: {}".format(buyer_name))
        print("Flight: {}-{}\n".format(air_weeks[0], flight_end_date))

        exemel_utils.update_proposal_header(air_weeks,call_letters)
        xml_folder = Path('./xml/')
        output_xml_file =  str(xml_folder / '{}_{}_{}_Proposal.xml'.format(est_num,call_letters,market_name))
        exemel_utils.write_to_proposal_xml(output_xml_file)
        exemel_utils.root.clear() # clears root of SubElements previously written

        exemel_utils.parser = exemel_utils.ET.XMLParser(remove_blank_text=True) #restores template_file as root
        exemel_utils.dom = exemel_utils.ET.parse(exemel_utils.template_file, exemel_utils.parser)
        exemel_utils.root = exemel_utils.dom.getroot()

    print("Process complete.")### The variable names / attributes of an object "Line" shown below are examples of the data that gets passed in as arguments to the create_exemel.create_xml_proposal_line() function.

if __name__ == "__main__":
    main()
