Q&A
===

Requirements: python3, pandas

1. Parse <course>-toknow.txt into database of questions and aswers by:

$ python parser.py toknows/<course>-toknow.txt databases/<course>-db.csv

for example, for NAT:

$ python parser.py toknows/nat-toknow.txt databases/nat-db.csv

This is to update the .csv database for the program to scrape questions and answers from. Needed when correcting grammar/vocab mistakes or adding questions in the <course>-toknow.txt file. 

2. Running q&a.py:

$ python q\&a.py

Follow instructions. For NAT:

press 2 and enter
press <topic number> and enter
when ready (Ready? in the screen) press enter
at each question press enter to see answer
at the ...Correct? statement press 1 to record correct answer, or 0/enter for incorrect 
*can press end to record answered questions and the stats at any moment, if you don't want to record results but need to leave just CTRL+C.

Stats are recorded in a csv, and the latest attempt will be shown at the start of each session. To view the full recorded stats just open using pandas to parse the csv. 
