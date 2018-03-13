Order_Input
v 1.0.1, 03/12/2018

This program was created to convert .pdf files containing radio scheduling
information into .xml files, which can then be imported using our proprietary order
scheduling software - Strata VIEW.
This eliminates the need to manually type in the order data by hand.


This script does the following:
1. Instantiates an object: "Order"  for each .pdf file in pdftoxml\\Orders\\ , which
contains associated objects: "Page", and "Line".

2. Parses each file, and identifies relevant bits of text using regular expressions,
then stores the text into different object/instance variables (attributes).
	ex:
		Line.spot_rate = "60"
		Line.daypart_program = " M 6:00a-10:00p

3. Uses the data stored in these variables to construct and save an XML Proposal
File to .\\xml\\


Installation:
- after cloning this repo, run the following within pdftoxml\\Order_Input\\ to
install required third party python modules / dependencies:

	$ pip install .

Directions:
1. Navigate to:
	pdftoxml\\Order_Input\\

	and run the following in the terminal:

		$ python input.py
2. The .xml files created will be saved to pdftoxml\\Order_Input\\xml\\filename.xml

-Thank you for your time.

 

