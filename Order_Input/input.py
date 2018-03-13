from datetime import time, date, timedelta, datetime
from isoweek import Week
import PyPDF2
import os
import re
import textwrap
import exemel

def main():


    class Order:
        #should instantiate an Order object. An order object can have a certain number of pages, with each page containing lines (roughly 10 or so per page)

        #attributes
        def __init__(self,file,pdfReader):
            self.file = file #'.\\Orders\\Dallas.pdf' absolute path to file
            self.pdfReader = pdfReader


        #methods    needs to be able to read a pdf object (inherits from PyPDF2)

        def get_number_of_pages(self):
            number_of_pages = self.pdfReader.numPages
            return number_of_pages


        def get_page_text(self): #creates a dictionary 'page_text',reads every page in a file, and sets the key as 'Page {#}' and the value as the string of text
            page_text = {}

            for page_num in range(0,self.get_number_of_pages()):
                pageObj = self.pdfReader.getPage(page_num)
                page_text["Page {}".format(page_num +1)] = pageObj.extractText()
            return page_text

        def get_call_letters(self):
            match = re.search(r'(K|W)\D{2,3}-(F|A)M',self.get_page_text()['Page 1'])
            match = match.group(0)
            return match

        def get_market_name(self):
            match = re.search(r'(.+)\nDescription',self.get_page_text()['Page 1']).group(1)
            return match

        def get_est_num(self):
            match = re.search(r'Product:\n(\d{4})',self.get_page_text()['Page 1']).group(1)
            return match

        def get_product_name(self):
            match = re.search(r'(.+)\nProduct:', self.get_page_text()['Page 1']).group(1)
            return match

        def get_buyer_name(self):
            match = re.search(r'(.+)\nBuyer:', self.get_page_text()['Page 1']).group(1)
            return match

        def __str__(self):
            return self.file.split('Orders\\')[1].split('.pdf')[0]






    class Page(Order):
    # needs to instantiate a new Page object for all pages in the order containing relevant schedule info. ex: should be values for spot_counts, spot_rates,

        def __init__(self, page_num, text,call_letters):
            super().__init__(self,pdfReader) # this is executing 10 times. Is there a way to store this to a variable so you only have to call once?
            self.call_letters = call_letters
            self.page_num = page_num
            self.text = text
        def __str__(self):
            return self.page_num



        def get_air_weeks(self): # returns a list of air weeks.
            air_weeks = []
            split_1 = self.text.split("\nDur")[1].split(self.call_letters)[0].split("\n")[1:-1]
            for wk in split_1:
                air_weeks.append(wk)
            return air_weeks

        def get_hiatus_weeks(self):
            iso_week_nums = []
            for week in self.get_air_weeks():
                dt = date(2018, int(week.split('/')[0]), int(week.split('/')[1]))
                wk = dt.isocalendar()[1]
                iso_week_nums.append(wk)

            index = 0
            hiatus_week_nums = []
            while index < len(iso_week_nums) - 1:
                if iso_week_nums[index + 1] - iso_week_nums[index] > 1:
                    week_before = iso_week_nums[index]
                    week_after = iso_week_nums[index + 1]
                    weeks_to_add = week_after - week_before - 1
                    for x in range(weeks_to_add):
                        week_before += 1
                        hiatus_week_nums.append(week_before)

                index += 1
            hiatus_weeks = []
            for week in hiatus_week_nums:
                d = Week(2018, week).monday()
                d = d.strftime('%m/%d')
                hiatus_weeks.append(d)
            return hiatus_weeks


        def get_week_nums(air_weeks): # returns the index position of the weeks with active flight spots
            week_dict = {}
            week = 1
            for wk in air_weeks:
                week_dict["Week {}".format(week)] = wk
                week +=1
            return week_dict


        def get_line_nums(self):
            matches = re.findall(r'(\d{1,2})\n.+\s{1,2}\d{1,2}:\d{2}.-\s*\n?\d{1,2}:\d{2}.',self.text)
            line_nums = []
            for ln in matches:
                line_nums.append(ln[0:])
            return line_nums


        def get_daypart_programs(self):
            text = self.text.replace("   ", '')
            matches = re.findall('((M|Tu|W|Th|F|Sa|Su|MTuWThFSaSu|MTu|TuW|WTh|ThF|MTuW|MTuWTh|MTuWThF|MTuWThFSa|TuWTh|TuWThF|TuWThFSa|TuWThFSaSu|WThFSa|WThF|WTh|WThFSaSu|ThFSaSu|FSaSu|FSa|SaSu)\s{1,2}\d{1,2}:\d{2}.-\s*\n?\d{1,2}:\d{2}.)', self.text)
            daypart_programs = []
            for m in matches:
                daypart_programs.append(m[0].replace('\n', ''))
            return daypart_programs

        def get_spot_rates(self):
            spot_rates = re.findall(r'.{1,2}\n(\$\d*,*\d{1,4}\.\d{2})', self.text)
            return spot_rates

        def get_daypart_symbols(self): 
            matches = re.findall(r'(MD|AM|PM|T|RT)\n\$\d*,*\d{1,4}\.\d{2}', self.text)
            symbols = []
            for m in matches:
                symbols.append(m[0:2].strip('\n'))

            return symbols

        def get_spot_durs(self):
            spot_durs = re.findall(r'.{1,2}\n\$\d*,*\d{1,4}\.\d{2}\n(\d{2})',self.text)
            return spot_durs

        def get_spot_counts(self):
            matches = re.findall(r'(.{1,2}\n\$\d*,*\d{1,4}\.\d{2}\n\d{2}\n(\d{1,4}\n)+)',self.text)
            spot_counts = []

            for sc in matches:
                spot_counts.append(sc[0].strip('\n').split('\n'))

            for sc in spot_counts:
                del sc[0:3]
                del sc[-1]
            return spot_counts

        def get_daypart_notes(self):
            matches = re.findall(r'.{1,2}\n\$\d*,*\d{1,4}\.\d{2}\n\d{2}\n(\d{1,4}\n)+(.+)', self.text)

            daypart_notes = []
            for note in matches:
                daypart_notes.append(note[1])

            return daypart_notes

           

        def page_with_spots(self):
            for dp in self.get_daypart_programs():
                if dp[1] in text:
                    return True
                else:
                    return False

        def last_page(self): # determines which pages contain active spot data
            if "Total Cost:" in self.text:
                return True
            else:
                return False
    ###

    class Line(Page):
        # instantiates an object "Line" for each line on every Page in the Order.

        num_of_lines = 0
        def __init__(self, line_num,daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count,daypart_note):
            super().__init__(self,text,call_letters)
            self.air_weeks = self.get_air_weeks()
            self.get_hiatus_weeks = self.get_hiatus_weeks()
            self.line_num = line_num
            self.daypart_program = daypart_program
            self.daypart_symbol = daypart_symbol
            self.spot_rate = spot_rate
            self.spot_dur = spot_dur
            self.spot_count = spot_count
            self.daypart_note = daypart_note


            Line.num_of_lines += 1

        def __str__(self):
            return self.line_num




    def get_flight_end_date(air_weeks):
        last_week = air_weeks[-1]
        month = int(last_week.split('/')[0])
        day = int(last_week.split('/')[1])

        dateObj = date(2018, month, day)
        flight_end_date = dateObj + timedelta(days=6)
        flight_end_date = flight_end_date.strftime('%m/%d')

        return flight_end_date.strip('0').replace('/0','/')


#---------------------------------
# Main program functionality

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
        order_objs['Order {}'.format(num_of_orders)] = Order(file,pdfReader) # Order class constructor

        current_order = order_objs['Order {}'.format(num_of_orders)] # stores the current order in the loop to a variable

        call_letters = current_order.get_call_letters()
        market_name = current_order.get_market_name()
        est_num = current_order.get_est_num()
        product_name = current_order.get_product_name()
        buyer_name = current_order.get_buyer_name()




        page_objs = {}

        for page_num, text in current_order.get_page_text().items(): # for each page in the order, create a page object
            page_objs['{}-{}'.format(current_order,page_num)] = Page(page_num, text,call_letters) # Page class constructor
            current_page = page_objs['{}-{}'.format(current_order,page_num)]



            if current_page.page_with_spots() == True: # if the current page contains a schedule with spots, then read it.
                air_weeks = current_page.get_air_weeks()
                hiatus_weeks = current_page.get_hiatus_weeks()


                # for each line, create a line object
                line_objs = {}

                flight_end_date = get_flight_end_date(air_weeks)
                exemel.endDate = exemel.get_endDate(air_weeks)
                exemel.startDate = exemel.get_startDate(air_weeks)

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
                    #import pdb;pdb.set_trace()
                    daypart_symbol = current_page.get_daypart_symbols()[b]
                    spot_rate = current_page.get_spot_rates()[b]
                    spot_dur = current_page.get_spot_durs()[b]
                    spot_count = current_page.get_spot_counts()[b]
                    daypart_note = current_page.get_daypart_notes()[b]
                    line_objs["{}-{}-Line {}".format(current_order.__str__(),current_page.__str__(),i)] = Line(line_num, daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note)
                    current_line = "{}-{}-Line {}".format(current_order.__str__(),current_page.__str__(),i)

                    b += 1
                    exemel.create_xml_proposal_line(line_objs[current_line],air_weeks,hiatus_weeks,market_name,file)

        print("\nOrder #{}: {}".format(num_of_orders, current_order))
        print("Market Name: {}".format(market_name))
        print("Call Letters: {}".format(call_letters))
        print("Estimate Number: {}".format(est_num))
        print("Product: {}".format(product_name))
        print("Buyer: {}".format(buyer_name))
        print("Flight: {}-{}\n".format(air_weeks[0], flight_end_date))

        exemel.update_proposal_header(air_weeks,call_letters)
        output_xml_file = '.\\xml\\{}_{}_{}_Proposal.xml'.format(est_num,call_letters,market_name)
        exemel.write_to_proposal_xml(output_xml_file)
        exemel.root.clear() # clears root of SubElements previously written

        exemel.parser = exemel.ET.XMLParser(remove_blank_text=True) #restores template_file as root
        exemel.dom = exemel.ET.parse(exemel.template_file, exemel.parser)
        exemel.root = exemel.dom.getroot()

    print("Process complete.")







if __name__ == "__main__":
    main()





### The variable names / attributes of an object "Line" shown below are examples of the data that gets passed in as arguments to the exemel.create_xml_proposal_line() function.
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


