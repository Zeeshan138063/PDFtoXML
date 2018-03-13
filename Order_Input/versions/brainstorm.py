import  PyPDF2, os
import re
import textwrap

#---- my external scripts
import exemel


def main():

    def get_page_text(pdfReader): #reads every page in a file, and stores the text as a string into a dictionary 'page_text'
        page_text = {}
        number_of_pages = pdfReader.numPages

        for page_num in range(0,number_of_pages):
            pageObj = pdfReader.getPage(page_num)
            page_text["Page {}\n".format(page_num +1)] = pageObj.extractText()
        return page_text


    def get_air_weeks(text,call_letters): # returns a list of air weeks.
        air_weeks = []
        split_1 = text.split("Dur")[1]
        split_2 = split_1.split(call_letters)[0]
        split_3 = split_2.split("\n")[1:-1]
        for wk in split_3:
            air_weeks.append(wk)
        return air_weeks

    def get_week_nums(air_weeks): # returns the index position of the weeks with active flight spots
        week_dict = {}
        week = 1
        for wk in air_weeks:
            week_dict["Week {}".format(week)] = wk
            week +=1
        return week_dict


    def get_call_letters(text):
        letters = re.compile(r'(.+)\nComments:')
        x = letters.search(text).group(1)
        return x

    def get_line_nums(text):
        matches = re.findall(r'(\d{1,2})\n.+\s{2}\d{1,2}:\d{2}.-\s*\n?\d{1,2}:\d{2}.',text)
        line_nums = []
        for ln in matches:
            line_nums.append(ln[0:])
        return line_nums


    def get_daypart_programs(text):
        text = text.replace("   ", '')
        matches = re.findall('((M|Tu|W|Th|F|Sa|Su|MTuWThFSaSu)\s{2}\d{1,2}:\d{2}.-\s*\n?\d{1,2}:\d{2}.)', text)
        daypart_programs = []
        for m in matches:
            daypart_programs.append(m[0].replace('\n', ''))
        return daypart_programs

    def get_spot_rates(text):
        spot_rates = re.findall(r'.{1,2}\n(\$\d{2,3}\.\d{2})', text)
        return spot_rates

    def get_daypart_symbols(text):
        symbols = re.findall(r'(.{1,2})\n\$\d{2,3}\.\d{2}', text)
        return symbols

    def get_spot_durs(text):
        spot_durs = re.findall(r'.{1,2}\n\$\d{2,3}\.\d{2}\n(\d{2})',text)
        return spot_durs

    def get_spot_counts(text):
        matches = re.findall(r'(.{1,2}\n\$\d{2,3}\.\d{2}\n\d{2}\n(\d{1,3}\n)+)',text)
        spot_counts = []

        for sc in matches:
            spot_counts.append(sc[0].strip('\n').split('\n'))

        for sc in spot_counts:
            del sc[0:3]
            del sc[-1]
        return spot_counts

    def get_daypart_notes(text):
        matches = re.findall(r'.{1,2}\n\$\d{2,3}\.\d{2}\n\d{2}\n(\d{1,3}\n)+(.+)',text)

        daypart_notes = []
        for note in matches:
            daypart_notes.append(note[1])

        return daypart_notes

       #define your variables here      Q--- Is this the correct spot in the code to store them?


    def page_with_spots(text,daypart_programs):
        for dp in daypart_programs:
            if dp[1] in text:
                return True
            else:
                return False

    def last_page(text): # need this to define where there are active spots in flight
        if "Total Cost:" in text:
            return True
        else:
            return False

    def get_talent_fees_per_month(): # should return the name of the month with the corresponding number of talent fees
        pass


    for page, text in get_page_text(pdfReader).items():
        #if last_page(text) == True: # need to also match text on pages that aren't last. if page contains daypart_programs:
        daypart_programs = get_daypart_programs(textwrap.dedent(text))

        if page_with_spots(text,daypart_programs) == True:

            line_nums = get_line_nums(text)
            call_letters = get_call_letters(text)
            air_weeks = get_air_weeks(text,call_letters)
            week_nums = get_week_nums(air_weeks)
            spot_rates = get_spot_rates(text)
            daypart_symbols = get_daypart_symbols(text)
            spot_durs = get_spot_durs(text)

            spot_counts = get_spot_counts(text)
            daypart_notes = get_daypart_notes(text)



            for line in line_nums: # for each line, execute the exemel.create_xml() function.
                #exemel.create_xml_line()                       # and use values from the above lists using a counter as the index num

                pass

            print('call_letters', call_letters, '\n')
            print('week_nums', week_nums)
            print('spot_rates', spot_rates, '\n')
            print('air_weeks', air_weeks, '\n')
            print('daypart_programs',daypart_programs, '\n')
            print('daypart_symbols',daypart_symbols, '\n')
            print('spot_durs',spot_durs, '\n')
            print('spot_counts',spot_counts, '\n')
            print('daypart_notes',daypart_notes, '\n')
            print('line_nums',line_nums, '\n')



if __name__ == "__main__":

    pdfFiles = []
    # for each pdf in the 'Orders' folder, add the filenames to a list pdfFiles.
    for filename in os.listdir('.\\Orders\\'):
        if filename.endswith('.pdf'):
            file_path = os.path.join("Orders",filename)
            pdfFiles.append(file_path)

    pdfFiles.sort(key=str.lower)  # sorted in alphabetical order


    for file in pdfFiles: # for each order pdf in the 'Orders' folder, create a pdf object and read the pdf.
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        main() # should have Order class constructor here Order()





#dallas.py notes
'''
       
    objective:
                  
                classes
                
                    class Order: # Order object (pdf with pages)
                        def __init__(self):
                        self.filename = filename
                        
                    
                    class Page(Order): #inherits from order
                        def 
                                       
                    class Line(Page): # inherits from Page
                        def __init__(self):
                            self.line_num = line_num
                            self.daypart_program = daypart_program
                            self.daypart_symbol = daypart_symbol
                            self.spot_rate = spot_rate
                            self.spot_dur = spot_dur
                            self.spot_count = spot_count
                            self.daypart_note = daypart_note
                            
                    for line in lines:
                        line = Line(line_nums[index], daypart_programs[index], daypart_symbols[index], spot_rates[index], spot_durs[index], spot_counts[index], daypart_notes[index])
                        
                    
                functions
                
                    see above ^
    
                helpful variables (string of text \ variable name (column from spreadsheet) \ location \ regex 
                
                    
                    Gourmet Foods \ product \ comes right after "Media:" and before "Product": \ #insert regex here
                
                    Dallas-Ft. Worth \ market_name \ comes immediately before line "Description:" \ "(.+)\nDescription:" matches group(1)
                    
                    Nolan LeGault \ buyer_name \ comes immediately before line "Buyer:" and after the line "Survey" \ "Survey:\n(.+)" matches group(1):
                    
                        
    
                    1/29 \ air_weeks #list containing wks on the schedule. \ first air week on schedule comes immediately after the line containing string "Dur:", \ "Dur\n(.+)" matches group(1):
                                                                                and lists out all weeks. Last week comes right before call_letters variable
                                                                                Show next date with
                                                                                
                        
                            
                    
                    KDGE-FM \ call_letters \ comes after last air_week and before "Comments:" line \ "(.+)\nComments:" matches group(1)
                    
                    #start of first row
                                        
                    1 \ line_num \ first occurrence of the string "1", comes directly after line containing "Comments: Talent fees listed below in gross. Please do not double book." \ #insert regex here
                    
                        M  6:00a-10:00a \ daypart_program \ comes directly after line_no \ (M|Tu|W|Th|F|Sa|Su|MTuWThFSaSu)\s{2}\d{1,2}:\d{2}.-\n?\d{1,2}:\d{2}. #if you extract the full match, this works
                        
                        AM \ daypart_symbol \ follows daypart_program \ (.{1,2})\n\$\d{2,3}\.\d{2}
                        
                        $300.00 \ spot_rate \ comes directly after daypart_symbol \.{1,2}\n(\$\d{2,3}\.\d{2})
                        
                        60 \ spot_dur \ immediately follows spot_rate \ .{1,2}\n\$\d{2,3}\.\d{2}\n(\d{2})
                        
                        0 \ spot_count \ immediately followers spot_dur. \ .{1,2}\n\$\d{2,3}\.\d{2}\n\d{2}\n(\d{1,3}\n)+
                        ----------------------------
                        0        1/29
                        1        2/5
                        3        2/12
                        0        4/30
                        1        5/7
                        
                        5       # total spots                     
                                The number at the top represents the first air_week from list air_weeks. ==  air_weeks[0] r'.{1,2}\n\$\d{2,3}\.\d{2}\n\d{2}\n(\d{1,3}\n)+'
                              These numbers move horizontally to the right on the schedule. 
                              
                        Josh Hart \ daypart_note \ immediately follows total spots \ .{1,2}\n\$\d{2,3}\.\d{2}\n\d{2}\n(\d{1,3}\n)+(.+)
                        
                        # end of row 1
                    
                    2    beginning of row 2, repeat all steps above. (Starting from "1" and all the way down to Josh Hart
                    
                    
                    
                    
                    variables on xml:
                    
                    
                    
                    
                    
                    To Do:
                    
                        1. Experiment with creating classes and implement into the program. - DONE (written to classes 2.py)                            
                        
                         2. 'get_air_weeks' function should convert week to same format as xml date string. - DONE
                         
                         3. call exemel.create_xml_line(template_file, output_xml_file, formatted_weeks, daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note) at the bottom of the script - DONE
                                - instead of passing all of these arguments, you can pass line["Line #"] object and call its attributes directly. This should look cleaner - DONE
                               
                                
                         4. write function or way to assign Monday.text = 'Y' if there's an 'M' in the daypart_program - DONE
                            - could create a dictionary like the below to determine what days there are spots. The key will be a daypart code such as "M-W" and the value will be :["M", "Tu", "W"]
                                {"M":"M","Tu":"Tu", "W":"W", 'Th':'Th', 'F':'F', 'Sa':'Sa', 'Su':'Su', 'M-W': ['M','Tu','W']} etc. etc. 
                                but before you do all of this, you need to identify all of the possible ways the pdfs will name a daypart. 
                                
                        5. Since this will output to one xml file, you will need to generate the appropriate header tags to accommodate for when there are > 1 pdf files. (This is not true for Proposal File. 
                            - maybe look into generating the xml for the spot radio file instead. 
                            - need to create functions to find the following header info
                                Proposal file
                                    {ex:/ variable name}
                                    - <Name>Radio Schedule - {market_name} 3BK {Oct17-Dec17 / } MSA ARB PPM</Name>
                                Radio Submission File
                                    - 
                            
                        7. End time for M-SU 6a-559a. 559 A should be comverted to 29:59. Also, StartTime needs to look like 06:00 (zero padded) - DONE
                        
                        8. Why are there no zeros printed in the order, and why is it splitting them up by line?
                            - Need script to not write <SpotsPerWeek> tag when there are 0 spots. * This might actually be optional. -DONE                        
                                - need to map out zeros for all of the hiatus weeks. 
                                - define a function that finds hiatus weeks, and stores them in a list # 
                                
                                
                        9 - Write in hiatus week functionality. (maybe add hiatus weeks into a dictionary with values set to string "0" - DONE
                        10. create Spot Radio xml writer
                        11. create proposal header template (will need to write 		from <Proposal> 		down to <TargetDemo>  - DONE
                        12. should have a date class or group of functions that works in both classes and exemel to call date format conversion  functions that are specific to this projects' format - DONE

                        13. Write in error handler which will notify the user when the spot counts don't match the number of air weeks. This happens when there's no zero listed on the order. 
                            Ask the user to type in the line no of which to insert the spot count value
                            or 
                            define a list of weeks and define as campaign_flight_weeks, which will represent the flight weeks for all orders in the folder. 
                            Then, once air_weeks is set for each order, check to see if wk in air_weeks is in campaign_flight_weeks.
                                if True, then spot counts will equal the spot count for the correct weeks,
                                else: assign "0" as the spot count for all other weeks. 
                        

                        14.  PM drive orders must contain time in PM format, otherwise, it will print the AM values. - DONE
                        
                        15. improve get daypart_symbols regex - DONE
                        16. Find a way to only make a user write where there should be zeros on the order, so the program can figure out the rest.

                                
                        Functionality Objectives:
                        
                                1. Associate talent name with their daypart, spot_rate and talent_fee and use this information to check 
                                iHeart internal Avail spreadsheets to make sure everything is the same
                                
                                2. Create function "get_talent_fees_per_month()" fees per month that totals the number of talent fees in a given month.
                                
                                3. Introduce command line interface package to improve functionality
                        
                        
                        
                        Control Flow / Wireframe 
                       
                            
                       
                            
                                bonus: check both the avail spreadsheet and endorsement tool database and print rates & info 
                                from all three sources (order,avail spreadsheet, endorsement too) to see if it matches. 
                                
                                - if you create a template for a standard excel/google sheet that we submit talents/stations to Ad Results, this program (or a script called immediately after) can check
                                    to make sure that all rates, talent fees, talent names, dayparts are the same. If they are the same, then place cleared orders in folder "Approved" 
                                
                        extras / thoughts for later:
                            - Create an iHeart Radio 2018 Annual Calendar (weeks starting on Monday)
                            

print output

4
2BK Nov17-Dec17 MSA ARB PPM
Clear Channel
KDGE-FM
Owner:
Date:
2018 Provide Commerce
Client:
Radio
Media:
Gourmet Foods
Product:
2577
2018 GF Local Test
60
Ad Results has first right of refusal on behalf of Provide Commerce until 12/31/18 for the year 20
19. Endorsers booked on mulitple Provide Commerce brands may be asked to change
creative between the brands.
1/1/2018
05:00 AM
12/30/2018
04:59 AM
Dallas-Ft. Worth
Description:
Separation between spots:
Market:
Estimate:
Flight Start Date:
Flight End Date:
Survey:
Nolan LeGault
Buyer:
Estimate Comments:
Tori Scott
214-866-8174
tori@kdge.com
Vendor:
Phone:
E-Mail:
KDGE-FM
Ad Results Media
Ad Results Media
320 Westcott St. Ste. 101
1/15/2018
Revision #:
Format:
Contact:
Rock
Vendor Code:
Send Billing To:
Houston, TX 77007
Phone:
713-783-1800
Buy Detail Report
Line
No
Daypart
Program
Daypart
Code
STN
Gross
Wks
Total
Spots
Dur
1/29
2/5
2/12
4/30
5/7
KDGE-FM
Comments: Talent fees listed below in gross. Please do not double book.
1
M  6:00a-10:00a
AM
$310.00
60
0
1
3
0
1
5
Josh Hart
2
Tu  6:00a-10:00a
AM
$310.00
60
0
2
1
1
2
6
Josh Hart
3
W  6:00a-10:00a
AM
$310.00
60
1
2
0
1
3
7
Josh Hart
4
Th  6:00a-10:00a
AM
$310.00
60
1
3
0
2
3
9
Josh Hart
5
F  6:00a-10:00a
AM
$310.00
60
1
3
0
2
0
6
Josh Hart
6
MTuWThFSaSu  6:00a-
5:59a
T
$205.88
60
1
1
1
1
1
5
Josh Hart Talent Fee
Total Spots:
4
12
5
7
10
38
Total Cost:
$11,259.40
38
Signature:
Disclaimer:
Please sign and fax to nolan@adresultsmedia.com.
This schedule has been built on gross rates. Ad Results must have fair and equal rotation. Rules o
f the Game apply to all orders. This order is void until signed and returned to Ad Results. All ch
anges to this order
must be approved by Ad Results in writing. Ad Results is liable for payment only to the extent tha
t we have been paid by the client. Host(s) shall not engage in any form of hate speech. Hate speec
h is defined as
a written, visual or verbal attack a person or group on the basis of attributes such as gender, et
hnic origin, religion, race, disability, or sexual orientation. Any engagement in this sort of Hat
e Speech shall result in
immediate cancellation. This order supersedes all previous orders for this client.  Œ NO DOUBLE LI
VES UNLESS AUTHORIZED BY AD RESULTS.
Page:
1
'''

