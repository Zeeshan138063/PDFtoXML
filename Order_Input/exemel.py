import os
import re
from lxml import etree as ET
from datetime import time, date, timedelta, datetime
from isoweek import Week
import collections

def parse_xml(root):
    for child in root.iter():
        if child.tag == '{http://www.AAAA.org/schemas/TVBGeneralTypes}CommentLine':
            print(child.text)


def get_formatted_weeks(air_weeks): #returns a list of strings named formatted_weeks
    formatted_weeks = []
    for wk in air_weeks:
        split = wk.split('/')
        month = int(split[0])
        day = int(split[1])
        d = date(2018, month, day)
        date_string = d.strftime("%Y-%m-%d")
        formatted_weeks.append(date_string)

    return formatted_weeks


def convert_AvailName(daypart_program): #converts daypart_program to same format as <AvailName> tag
    new = ''
    if ":00" in daypart_program:
        old = ":00"
        daypart_program = daypart_program.replace(old,new)
    if ":30" in daypart_program or ":15" in daypart_program or ":45" in daypart_program:
        old = ":"
        daypart_program = daypart_program.replace(old,new)
    if "MTuWThFSaSu" in daypart_program:
        daypart_program = daypart_program.replace("MTuWThFSaSu","M-Su")
    daypart_program = daypart_program.replace("  "," ").replace("- ",'-')
    return daypart_program

def convert_SpotLength(spot_dur): #converts spot_dur to proper xml format for element 'SpotLength'

    if spot_dur == "60":
        minutes = 1
        seconds = 0
    else:
        minutes = 0
        seconds = int(spot_dur)

    t = time(0, minutes, seconds)
    SpotLength = t.strftime("%H:%M:%S")

    return SpotLength

def get_start_time(daypart_program):

    start = re.search(r'\d{1,2}:\d{2}', daypart_program).group(0)
    hour = int(start.split(":")[0])
    minute = int(start.split(":")[1])

    if "p" in daypart_program.split("-")[0] and "12:" not in daypart_program.split("-")[0]:
        hour += 12
    st = time(hour,minute)
    StartTime = st.strftime("%H:%M")

    return StartTime

def get_end_time(daypart_program):
    end = re.search(r'-\s*(\d{1,2}:\d{2}).',daypart_program).group(1)
    hour = int(end.split(":")[0])
    minute = int(end.split(":")[1])
    if hour == 5 and minute == 59:
        EndTime = "29:59"
    else:
        if "p" in daypart_program.split("-")[1] and "12:" not in daypart_program.split("-")[1]:
            hour += 12
        et = time(hour,minute)
        EndTime = et.strftime("%H:%M")

    return EndTime

def get_startDate(air_weeks):
    startDate = get_formatted_weeks(air_weeks)[0]
    return startDate



def get_endDate(air_weeks):
    endDate = convert_dateObj_to_string(convert_string_to_dateObj(get_formatted_weeks(air_weeks)[-1]) + timedelta(days=6))
    return endDate


def convert_string_to_dateObj(air_week):  # converts formatted week string to dateObj
    split_string = air_week.split('-')
    year = int(split_string[0])
    month = int(split_string[1])
    day = int(split_string[2])

    dateObj = date(year, month, day)

    return dateObj


def convert_dateObj_to_string(dateObj):
    date_string = dateObj.strftime('%Y-%m-%d')

    return date_string



def get_all_weeks(air_weeks, hiatus_weeks,spot_count,line_num,file): # returns a dictionary of all weeks (both air weeks and hiatus) with the value = the number of spots for that week
    formatted_air_weeks = get_formatted_weeks(air_weeks)
    formatted_hiatus_weeks = get_formatted_weeks(hiatus_weeks)
    all_weeks = {}

    if len(spot_count) != len(air_weeks):
        os.startfile(file)
        revised_spot_count = get_revised_spot_count(air_weeks,spot_count,line_num)
        spot_count = revised_spot_count

    index = 0
    for week in formatted_air_weeks:
        all_weeks[week] = spot_count[index]
        index +=1
    for hiatus_week in formatted_hiatus_weeks:
        all_weeks[hiatus_week] = "0"
    ordered = collections.OrderedDict(sorted(all_weeks.items(), key=lambda t: t[0]))

    return ordered

def get_revised_spot_count(air_weeks, spot_count, line_num):
   # if the length of the line with spot count numbers is not equal to the number of air_weeks
    awks_and_sptc = {}

    s_length = len(spot_count)
    print("Whoops, looks like a human didn't put a '0' where there should be...\t¯\_(ツ)_/¯\n")

    get_zero_weeks = input(
        "For line #{}, please type in the week number(s) that contains 0 spots. (ex: 5/7)\n\tuse ',' as a delimiter\n>".format(
            line_num))
    for week in air_weeks:
        awks_and_sptc[week] = ""

    for wk in get_zero_weeks.split(','):
        awks_and_sptc[wk] = "0"
        spot_count.append("0")

    while True:
        values_list = []
        i = 0
        for key, value in awks_and_sptc.items():
            if value != "0":
                awks_and_sptc[key] = spot_count[i]
                i += 1

        if len(spot_count) == len(air_weeks):
            break

    for value in awks_and_sptc.values():
        values_list.append(value)

    return values_list



def create_xml_proposal_line(line,air_weeks,hiatus_weeks,market_name,file): #air_weeks, daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note): # construct a new xml file from the template.xml file, which consists of ElementTree objects that contain nested elements representing spot_rate, daypart_program, daypart_symbol, spot_dur, spot_count
    startDate = get_startDate(air_weeks)
    endDate = get_endDate(air_weeks)
    name = 'Radio Schedule - {} 3BK Oct17-Dec17 MSA ARB PPM'.format(market_name)

    for child in root.iter():
        if child.tag == '{http://www.AAAA.org/schemas/spotTVCableProposal}AvailList':
            AvailList = child
            AvailList.attrib['startDate'] = startDate
            AvailList.attrib['endDate'] = endDate
            AvailList.attrib['name'] = name

    for child in AvailList.iter():
        if child.tag == '{http://www.AAAA.org/schemas/spotTVCableProposal}Name':
            child.text = name

    #TargetDemo = ET.SubElement(AvailList, '{http://www.AAAA.org/schemas/spotTVCableProposal}OutletReference',{'demoRef':'DMO'})
    AvailLineWithDetailedPeriods = ET.SubElement(AvailList,'{http://www.AAAA.org/schemas/spotTVCableProposal}AvailLineWithDetailedPeriods')
    OutletReference = ET.SubElement(AvailLineWithDetailedPeriods,'{http://www.AAAA.org/schemas/spotTVCableProposal}OutletReference',{'outletFromListRef':'OUL0'})

    DayTimes = ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}DayTimes')
    DayTime = ET.SubElement(DayTimes, '{http://www.AAAA.org/schemas/spotTVCableProposal}DayTime')

    StartTime = ET.SubElement(DayTime, '{http://www.AAAA.org/schemas/spotTVCableProposal}StartTime')
    StartTime.text = get_start_time(line.daypart_program)

    EndTime = ET.SubElement(DayTime, '{http://www.AAAA.org/schemas/spotTVCableProposal}EndTime')
    EndTime.text = get_end_time(line.daypart_program)

    Days = ET.SubElement(DayTime, '{http://www.AAAA.org/schemas/spotTVCableProposal}Days')

    Monday = ET.SubElement(Days,'{http://www.AAAA.org/schemas/TVBGeneralTypes}Monday')
    Tuesday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Tuesday')
    Wednesday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Wednesday')
    Thursday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Thursday')
    Friday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Friday')
    Saturday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Saturday')
    Sunday = ET.SubElement(Days, '{http://www.AAAA.org/schemas/TVBGeneralTypes}Sunday')


    day_of_week = line.daypart_program.split('  ')[0].strip()
    day_dict = {"M":Monday,"Tu":Tuesday,'W':Wednesday,'Th':Thursday,'F':Friday,"Sa":Saturday,'Su':Sunday}
    for key, value in day_dict.items():
        if key in day_of_week:
            value.text = 'Y'
        elif day_of_week == "MTuWThFSaSu":
            value.text = 'Y'

        else:
            value.text ='N'

    DaypartName = ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}DaypartName')
    DaypartName.text = line.daypart_symbol
    AvailName = ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}AvailName')
    AvailName.text = convert_AvailName(line.daypart_program)
    SpotLength = ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}SpotLength')
    SpotLength.text = convert_SpotLength(line.spot_dur)

    Comment = ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}Comment')
    CommentLine = ET.SubElement(Comment,'{http://www.AAAA.org/schemas/TVBGeneralTypes}CommentLine')
    CommentLine.text = line.daypart_note

    Periods =  ET.SubElement(AvailLineWithDetailedPeriods, '{http://www.AAAA.org/schemas/spotTVCableProposal}Periods')

    all_weeks = get_all_weeks(air_weeks,hiatus_weeks,line.spot_count,line.line_num,file)

    for wk,spt_c in all_weeks.items():

        last_day = lambda x: datetime.strptime(wk.replace('-', ''), "%Y%m%d").date() + timedelta(days=6)
        last_day_string = last_day(wk).strftime("%Y-%m-%d")

        DetailedPeriod = ET.SubElement(Periods, '{http://www.AAAA.org/schemas/spotTVCableProposal}DetailedPeriod',{'startDate':wk,'endDate':last_day_string})
        Rate = ET.SubElement(DetailedPeriod, '{http://www.AAAA.org/schemas/spotTVCableProposal}Rate')
        Rate.text = line.spot_rate.replace("$","")

        if spt_c != '0':
            SpotsPerWeek = ET.SubElement(DetailedPeriod,
                                         '{http://www.AAAA.org/schemas/spotTVCableProposal}SpotsPerWeek')
            SpotsPerWeek.text = spt_c

        DemoValues = ET.SubElement(DetailedPeriod,'{http://www.AAAA.org/schemas/spotTVCableProposal}DemoValues')
        DemoValue = ET.SubElement(DemoValues, '{http://www.AAAA.org/schemas/spotTVCableProposal}DemoValue', {'demoRef':'DM0'})
        DemoValue.text = "0.22"


def update_proposal_header(air_weeks,call_letters): # for each order in the directory, create a header and write to the file above the order lines
    startDate = get_startDate(air_weeks)
    endDate = get_endDate(air_weeks)

    for child in root.iter():
        if child.tag == '{http://www.AAAA.org/schemas/spotTVCableProposal}Proposal':
            Proposal = child
            Proposal.attrib["startDate"] = startDate
            Proposal.attrib["endDate"] = endDate

    for child in Proposal.iter():
        if child.tag == '{http://www.AAAA.org/schemas/spotTVCableProposal}Outlets':
            Outlets = child
    for child in Outlets.iter():
        if child.tag == '{http://www.AAAA.org/schemas/spotTVCableProposal}RadioStation':
            RadioStation = child
            RadioStation.attrib['callLetters'] = call_letters.split('-')[0]
            RadioStation.attrib['band'] = call_letters.split('-')[1]



'''
def create_radio_spot_order_header(line,air_weeks,hiatus_weeks): # for each order in the directory, create a header and write to the file above the order lines
    # add Radio Spot Order code here
'''

def write_to_proposal_xml(output_xml_file=".\\xml\\proposal.xml"):
    tree = ET.ElementTree(root)
    ET.register_namespace('tvb',"http://www.AAAA.org/schemas/spotTV")
    ET.register_namespace('tvb-tp',"http://www.AAAA.org/schemas/TVBGeneralTypes")
    #ET.register_namespace('',"http://www.AAAA.org/schemas/spotTVCableProposal") # only needed with xml.etree.ElementTree package
    tree.write(output_xml_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
    print("Proposal XML has been saved to {}\n".format(output_xml_file))



def write_to_radio_spot_order_xml(output_xml_file=".\\xml\\radio submission.xml"):
    tree = ET.ElementTree(root)
    ET.register_namespace('tvb',"http://www.AAAA.org/schemas/spotTV")
    ET.register_namespace('tvb-tp',"http://www.AAAA.org/schemas/TVBGeneralTypes")
    #ET.register_namespace('',"http://www.AAAA.org/schemas/spotTVCableProposal") # only needed with xml.etree.ElementTree package
    tree.write(output_xml_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
    print("Radio Spot Order XML has been saved to {}".format(output_xml_file))




while True:
    template_file = input("Press 'R' to create a radio spot order xml file. \n or press 'P' to create a proposal xml file.\n> ")

    if template_file.upper() == 'R':
        template_file = os.path.join('xml\\Templates', 'radio spot order template.xml')
        print('\nThis feature has not been set up yet. Program will produce a proposal xml.\n')
        template_file = os.path.join('xml\\Templates', 'proposal template.xml')
        break

    elif template_file.upper() == 'P':
        template_file = os.path.join('xml\\Templates', 'proposal template.xml')
        break
    else:
        print("\nIncorrect key command. Please try again...")



endDate = ''
startDate = ''

parser = ET.XMLParser(remove_blank_text=True)
dom = ET.parse(template_file, parser)
root = dom.getroot()





def main():
    parse_xml(root)
    #create_proposal_header()
    create_xml_proposal_line(Line,Line.air_weeks, Line.hiatus_weeks,market_name)

    new_xml = write_to_proposal_xml()




if __name__ == '__main__':
    class Line:
        file_name = 'TEST Proposal.xml'
        file_name_2 = "proposal template.xml"
        full_file = os.path.join("xml", file_name)
        call_letters = "KMAG-FM"
        template_file = os.path.join('xml\\Templates', 'proposal template.xml')
        air_weeks = ['3/5','3/19']
        daypart_program = 'M-Su  5:00a-12:00a'
        daypart_symbol = "RT"
        spot_rate = "0"
        spot_dur = '15'
        spot_count = ['5', '5']
        daypart_note = 'Bonus Weight'
        market_name = "Ft. Smith"




    main()


#notes
