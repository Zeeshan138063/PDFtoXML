import PyPDF2
import os
import re
import textwrap
import exemel_utils
import pdf_parse


def main():
    pdfFiles = []
    # for each pdf in the 'Orders' folder, add the filenames to a list pdfFiles.
    for filename in os.listdir('.\\Orders\\'):
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

        call_letters = current_order.get_call_letters()
        market_name = current_order.get_market_name()
        est_num = current_order.get_est_num()
        product_name = current_order.get_product_name()
        buyer_name = current_order.get_buyer_name()




        page_objs = {}

        for page_num, text in current_order.get_page_text().items(): # for each page in the order, create a page object
            page_objs['{}-{}'.format(current_order,page_num)] = pdf_parse.Page(page_num, text,call_letters,pdfReader) # Page class constructor
            current_page = page_objs['{}-{}'.format(current_order,page_num)]



            if current_page.page_with_spots() == True: # if the current page contains a schedule with spots, then read it.
                air_weeks = current_page.get_air_weeks()
                hiatus_weeks = current_page.get_hiatus_weeks()


                # for each line, create a line object
                line_objs = {}

                flight_end_date = pdf_parse.get_flight_end_date(air_weeks)
                exemel_utils.endDate = exemel_utils.get_endDate(air_weeks)
                exemel_utils.startDate = exemel_utils.get_startDate(air_weeks)

                # For Debugging only
                '''
                print(current_page.get_daypart_symbols())
                print(current_page.get_spot_rates())
                print(current_page.get_spot_durs())
                print(current_page.text)
                '''

                b = 0

                for i in current_page.get_line_nums(): # for each line on the page,
                    line_num = current_page.get_line_nums()[b]
                    daypart_program = current_page.get_daypart_programs()[b]
                    daypart_symbol = current_page.get_daypart_symbols()[b]
                    spot_rate = current_page.get_spot_rates()[b]
                    spot_dur = current_page.get_spot_durs()[b]
                    spot_count = current_page.get_spot_counts()[b]
                    daypart_note = current_page.get_daypart_notes()[b]
                    line_objs["{}-{}-Line {}".format(current_order.__str__(),current_page.__str__(),i)] = pdf_parse.Line(line_num, daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note,text,call_letters,pdfReader)
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
        output_xml_file = '.\\xml\\{}_{}_{}_Proposal.xml'.format(est_num,call_letters,market_name)
        exemel_utils.write_to_proposal_xml(output_xml_file)
        exemel_utils.root.clear() # clears root of SubElements previously written

        exemel_utils.parser = exemel_utils.ET.XMLParser(remove_blank_text=True) #restores template_file as root
        exemel_utils.dom = exemel_utils.ET.parse(exemel_utils.template_file, exemel_utils.parser)
        exemel_utils.root = exemel_utils.dom.getroot()

    print("Process complete.")### The variable names / attributes of an object "Line" shown below are examples of the data that gets passed in as arguments to the create_exemel.create_xml_proposal_line() function.




if __name__ == "__main__":
    main()

'''
call_letters = 'KDGE-FM'
air_weeks = ['1/29', '2/5', '2/12', '4/30', '5/7']

line_nums = ['1', '2', '3', '4', '5', '6']
daypart_programs = ['M  6:00a-10:00a', 'Tu  6:00a-10:00a', 'W  6:00a-10:00a', 'Th  6:00a-10:00a', 'F  6:00a-10:00a', 'MTuWThFSaSu  6:00a- 5:59a']
daypart_symbols = ['AM', 'AM', 'AM', 'AM', 'AM', 'T']
spot_rates = ['$310.00', '$310.00', '$310.00', '$310.00', '$310.00', '$205.88']
spot_durs = ['60', '60', '60', '60', '60', '60']
spot_counts = [['0', '1', '3', '0', '1'], ['0', '2', '1', '1', '2'], ['1', '2', '0', '1', '3'], ['1', '3', '0', '2', '3'], ['1', '3', '0', '2', '0'], ['1', '1', '1', '1', '1']]
daypart_notes = ['Josh Hart', 'Josh Hart', 'Josh Hart', 'Josh Hart', 'Josh Hart', 'Josh Hart Talent Fee']

'''