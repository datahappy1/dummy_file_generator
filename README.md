# dummy_file_generator
## Dummy .csv or .flat files generator in Python 3

This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).

## How to setup a project in this tool
Based on the datasets in your data_files directory, the tool loops through and generates the output files based on the following logic:
Let's say you need to generate a dummy file containing 3 columns, Names, Dates and IDs. You set the column names, in case it's a flat file you setup the column lenghts and the data_file files accordingly inside the config.json file. 

Let's assume your data_files txt files look like these 3 below:

Names.txt:  <br />
Frank  <br />
Paul  <br />
John  <br />

Dates.txt:  <br />
2017-12-30  <br />
2016-01-12  <br />
2015-11-11  <br />
2008-01-03  <br />

IDs.txt:  <br />
123456789  <br />
987654321  <br />
123  <br />
456  <br />
AA123987  <br />
AB3645  <br />

The output file will be written like:

##.txt flat file:
(considering column length is setup in config.json like Name:6 , Date:10, ID: 9) 

|Name--|Date------|ID-------|<br />
|Frank |2017-12-30|123456789|<br />
|Paul  |2016-01-12|987654321|<br />
|John  |2015-11-11|123      |<br />
|Frank |2008-01-03|456      |<br />
|Paul  |2017-12-30|AA123987 |<br />
|John  |2016-01-12|AB3645   |<br />

* Without the pipes and colons ofcourse:)

##.csv file:

Name,Date,ID<br />
Frank,2017-12-30,123456789<br />
Paul,2016-01-12,987654321<br />
John,2015-11-11,123<br />
Frank,2008-01-03,456<br />
Paul,2017-12-30,AA123987<br />
John,2016-01-12,AB3645<br />


## How to run this tool
The required arguments are :

projectname -pn <br />
filename -fn <br />
filesize -fs (in kB)

The optional arguments are :
generated_files_location -gf <br />

Run as:
`python __main__.py -pn dummy1 -fn dummy1file.csv -fs 256`

Pytest unit, integration and performance testing is also a part of this tool.
Run `pip install pytest` and then just run the command `pytest` in the project folder
