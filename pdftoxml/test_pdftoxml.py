import unittest
import pdftoxml
import pdf_parse
import exemel_utils

#the tests below check the main methods contained in pdftoxml.py and pdf_parse.py

class TestLearn(unittest.TestCase):

    # setup & teardown

    def setUp(self):
        self.page_1 = pdf_parse.Page("1","text", "KTSM-FM")


    #exemel_utils
    def test_get_formatted_weeks(self): #method must start with the word test, so this module knows that it is a test.
        actual_1 = exemel_utils.get_formatted_weeks(["3/19", "3/26", "4/9"])
        actual_2 = exemel_utils.get_formatted_weeks(["5/7", "6/4", "7/9", "8/13"])

        expected_1 = ["2018-03-19", "2018-03-26", "2018-04-09"]
        expected_2 = ["2018-05-07", "2018-06-04", "2018-07-09", "2018-08-13"]

        self.assertListEqual(expected_1, actual_1)
        self.assertListEqual(expected_2, actual_2)

    def test_get_start_time(self):
        actual_1 = exemel_utils.get_start_time("MTuWThF  5:30a- 9:00a")
        actual_2 = exemel_utils.get_start_time("MTuWThF 5:15a-9:45a")
        actual_3 = exemel_utils.get_start_time("MTuW 12:15a-9:45a")

        expected_1 = "05:30"
        expected_2 = "05:15"
        expected_3 = "00:15"

        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

    def test_get_end_time(self):
        actual_1 = exemel_utils.get_end_time("MTuWThF  5:30a- 9:00a")
        actual_2 = exemel_utils.get_end_time("MTuWThF 5:15a-9:45a")
        actual_3 = exemel_utils.get_end_time("MTuW 12:15a-12:00p")

        expected_1 = "09:00"
        expected_2 = "09:45"
        expected_3 = "12:00"

        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)


    #pdfparse - Order methods

    def test_get_call_letters(self):

        text_1 = "4/30\n5/7\nWAEB-AM\nComments: The talent fee for personality(s)"
        text_2 ="4/30\n5/7\nWAEB-PM\nComments: The talent fee for personality(s)"
        text_3 = "4/30\n5/7\nEFWAEB-AMXFG\nComments: The talent fee for personality(s)"

        actual_1 = pdf_parse.Order.get_call_letters(text_1)
        actual_2 = pdf_parse.Order.get_call_letters(text_2)
        actual_3 = pdf_parse.Order.get_call_letters(text_3)

        expected = "WAEB-AM"

        self.assertEqual(expected, actual_1)
        self.assertRaisesRegex(AttributeError, expected, actual_2)
        self.assertEqual(expected, actual_3)

    def test_get_market_name(self):
        text_1 = "Milwaukee-Racine\nSeparation between spots:\nMarket:"
        text_2 = "12/30/201804:59 AM\nMilwaukee-Racine\nDescription:Separation between spots:Market:"
        expected = "Milwaukee-Racine"

        actual_1 = pdf_parse.Order.get_market_name(text_1)
        actual_2 = pdf_parse.Order.get_market_name(text_2)


        self.assertRaisesRegex(AttributeError, expected, actual_1)
        self.assertEqual(expected, actual_2)

    def test_get_est_num(self):
        text_1 = "Product:\n2577\n2018 GF Local Test\n60"
        text_2 = "\n2577\n2018 GF Local Test\n60"
        text_3 = "Product:  \n2577"

        expected = "2577"

        actual_1 = pdf_parse.Order.get_est_num(text_1)
        actual_2 = pdf_parse.Order.get_est_num(text_2)
        actual_3 = pdf_parse.Order.get_est_num(text_3)

        self.assertEqual(expected, actual_1)
        self.assertRaisesRegex(AttributeError, expected, actual_2)
        self.assertNotEqual(expected, actual_3)

    def test_get_product_name(self):
        text_1 = "Media:\nGourmet Foods\nProduct:\n2577\n2018 GF Local Test\n"
        text_2 = "Media:\nGourmet FoodsProduct"
        text_3 = "asgadjhasjGourmet Foods\nProduct:\n2577\n2018 GF Local Test\n"

        expected = "Gourmet Foods"

        actual_1 = pdf_parse.Order.get_product_name(text_1)
        actual_2 = pdf_parse.Order.get_product_name(text_2)
        actual_3 = pdf_parse.Order.get_product_name(text_3)

        self.assertEqual(expected, actual_1)
        self.assertRaisesRegex(AttributeError, expected, actual_2)
        self.assertNotEqual(expected, actual_3)

    def test_get_buyer_name(self):
        text_1 = "Survey:\nKelsey Whittington\nBuyer:\nEstimate Comments:\n414-944-5144"
        text_2 = "Survey:\nKelsey WhittingtonEstimate Comments:\n414-944-5144"
        text_3 = "Survey:Kelsey Whittington\nBuyer"

        expected = "Kelsey Whittington"

        actual_1 = pdf_parse.Order.get_buyer_name(text_1)
        actual_2 = pdf_parse.Order.get_buyer_name(text_2)
        actual_3 = pdf_parse.Order.get_buyer_name(text_3)

        self.assertEqual(expected, actual_1)
        self.assertRaisesRegex(AttributeError, expected, actual_2)
        self.assertNotEqual(expected, actual_3)

    #pdf parse - Page methods
    def test_get_air_weeks(self):
        expected = ['1/29', '2/5', '2/12', '4/30', '5/7']

        self.page_1.text = "\nDur\n1/29\n2/5\n2/12\n4/30\n5/7\nKTSM-FM\nComments: Talent fees listed below in gross. Please do not double book.\n7\nM  3:00p- 6:00p"
        actual_1 = pdf_parse.Page.get_air_weeks(self.page_1)
        self.assertEqual(expected, actual_1)

        self.page_1.text = "\n1/29\n2/5\n2/12\n4/30\n5/7\nKTSM-FM\nComments: Talent fees listed below in gross. Please do not double book.\n7\nM  3:00p- 6:00p"
        actual_2 = pdf_parse.Page.get_air_weeks(self.page_1)
        self.assertRaises(IndexError)

    def test_get_hiatus_weeks(self):
        air_weeks_1 = ['1/29', '2/5', '2/12', '4/30', '5/7']
        air_weeks_2 = ['1/29', '2/5', '2/12', '4/30', '5/7','5/21']
        air_weeks_3 = ['1/29', '2/5','4/30', '5/7','5/21']

        expected_1 = ['02/19', '02/26', '03/05', '03/12', '03/19', '03/26', '04/02', '04/09', '04/16', '04/23']
        expected_2 = ['02/19', '02/26', '03/05', '03/12', '03/19', '03/26', '04/02', '04/09', '04/16', '04/23', '05/14']
        expected_3 = ['02/12', '02/19', '02/26', '03/05', '03/12', '03/19', '03/26', '04/02', '04/09', '04/16', '04/23', '05/14']


        actual_1 = pdf_parse.Page.get_hiatus_weeks(air_weeks_1)
        actual_2 = pdf_parse.Page.get_hiatus_weeks(air_weeks_2)
        actual_3 = pdf_parse.Page.get_hiatus_weeks(air_weeks_3)

        self.assertListEqual(expected_1, actual_1)
        self.assertListEqual(expected_2, actual_2)
        self.assertListEqual(expected_3, actual_3)

    def






if __name__ == "__main__": # this allows us to run python test_learn.py and will give us the same result as above.
    unittest.main()



