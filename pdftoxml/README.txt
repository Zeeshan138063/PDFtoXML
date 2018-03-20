Order_Input
v 1.0.1, 03/12/2018

NOTE
This is currently only supported on Windows operating systems. Unix support is in progress. Please check back soon.

PdftoXml was created to convert .pdf files containing radio scheduling information into .xml files, which can then be imported using iHeart's proprietary order scheduling software - Strata VIEW.
This eliminates the need to manually type in the order data by hand.


## What it does:
- Instantiates an object: "Order"  for each .pdf file in pdftoxml\\Orders\\ , which contains associated objects: "Page", and "Line".

- Parses each file, and identifies relevant bits of text using regular expressions, then stores the text into different object/instance variables (attributes).
	ex:
		Line.spot_rate = "60",
		Line.daypart_program = " M 6:00a-10:00p

- Uses the data stored in these variables to construct and save an XML Proposal File to .\\xml\\ 


##Installation:
- after cloning this repo, run the following within pdftoxml\pdftoxml\\ to install required third party python modules / dependencies:

	$ pip install .

##Directions:

- Navigate to:
	pdftoxml\\pdftoxml\\
	
- Run the following in the terminal:
		$ python pdftoxml.py
		
- The .xml files created will be saved to pdftoxml\\pdftoxml\\xml\\filename.xml

-Thank y