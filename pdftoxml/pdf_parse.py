from datetime import time, date, timedelta, datetime
from isoweek import Week
import PyPDF2
import os
import re
import textwrap
import exemel_utils
from pathlib import Path


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

    @staticmethod
    def get_call_letters(text):
        match = re.search(r'(K|W)\D{2,3}-(F|A)M',text)
        if match is not None:
            match = match.group(0)
        return match

    @staticmethod
    def get_market_name(text):
        match = re.search(r'(.+)\nDescription',text)
        if match is not None:
            match = match.group(1)
        return match

    @staticmethod
    def get_est_num(text):
        match = re.search(r'Product:\n(\d{4})',text)
        if match is not None:
            match = match.group(1)
        return match

    @staticmethod
    def get_product_name(text):
        match = re.search(r'(.+)\nProduct:', text)
        if match is not None:
            match = match.group(1)
        return match

    @staticmethod
    def get_buyer_name(text):
        match = re.search(r'(.+)\nBuyer:', text)
        if match is not None:
            match = match.group(1)
        return match

    def __str__(self):
        order_folder_string = str(Path('//'))
        split_1 = self.file.split(order_folder_string)[-1].split('.pdf')[0]
        return split_1






class Page(Order):
# needs to instantiate a new Page object for all pages in the order containing relevant schedule info. ex: should be values for spot_counts, spot_rates,

    def __init__(self, page_num, text, call_letters):
        self.call_letters = call_letters
        self.page_num = page_num
        self.text = text
    def __str__(self):
        return self.page_num



    def get_air_weeks(self): # returns a list of air weeks.
        air_weeks = []
        try:
            split_1 = self.text.split("\nDur")[1].split(self.call_letters)[0].split("\n")[1:-1]
            for wk in split_1:
                air_weeks.append(wk)
            return air_weeks
        except IndexError:
            return IndexError

    @staticmethod
    def get_hiatus_weeks(air_weeks):
        iso_week_nums = []
        for week in air_weeks:
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
            if dp[1] in self.text:
                return True
            else:
                return False

    def last_page(self): # determines which pages contain active spot data
        if "Total Cost:" in self.text:
            return True
        else:
            return False
    @staticmethod
    def get_flight_end_date(air_weeks):
        last_week = air_weeks[-1]
        month = int(last_week.split('/')[0])
        day = int(last_week.split('/')[1])

        dateObj = date(2018, month, day)
        flight_end_date = dateObj + timedelta(days=6)
        flight_end_date = flight_end_date.strftime('%m/%d')

        return flight_end_date.strip('0').replace('/0', '/')
###

class Line(Page):
    # instantiates an object "Line" for each line on every Page in the Order.

    num_of_lines = 0
    def __init__(self, line_num,daypart_program, daypart_symbol, spot_rate, spot_dur, spot_count, daypart_note, page_num, text, call_letters): # do text and call letters need to be passed here and in the inheritance call below? (super)
        super().__init__(page_num, text, call_letters)
        self.air_weeks = self.get_air_weeks()
        self.get_hiatus_weeks = self.get_hiatus_weeks(self.air_weeks)
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










