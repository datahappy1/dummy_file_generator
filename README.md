# dummy_file_generator
## Dummy .csv or .flat files generator in Python 3

This tool is able to generate dummy csv or flat txt files based on the config.json file settings you setup for your projects.

## How to setup a project in this tool
Based on the datasets in your data_files directory, the tool loops through and generates the output files based on the following logic:
Let's say you need to generate a dummy file containing 3 columns, Names, Dates and IDs. You set the column names, in case it's a flat file you setup the column lenghts and the data_file files accordingly inside the config.json file. 

Let's assume your data_files txt files look like these 3 below:

Names.txt:
Frank
Paul
John

Dates.txt:
2017-12-30
2016-01-12
2015-11-11
2008-01-03

IDs.txt:
123456789
987654321
123
456
AA123987
AB3645

The output file will be written like:

##.txt flat file:
(considering column length is setup in config.json like Name:6 , Date:9, ID: 9) 

Name  Date       ID         
Frank 2017-12-30 123456789\n
Paul  2016-01-12 987654321
John  2015-11-11 123      
Frank 2008-01-03 456      
Paul  2017-12-30 AA123987 
John  2016-01-12 AB3645   

##.csv file:

Name,Date,ID
Frank,2017-12-30,123456789
Paul,2016-01-12,987654321
John,2015-11-11,123
Frank,2008-01-03,456
Paul,2017-12-30,AA123987
John,2016-01-12,AB3645


## How to run this tool
The required arguments are :

projectname -pn 
filename -fn
filesize -fs (in kB)

The optional arguments are :
generated_files_location -gf

Run as:
`python __main__.py -pn dummy1 -fn dummy1file.csv -fs 256`

Pytest unit, integration and performance testing is also a part of this tool.
Run `pip install pytest` and then just run the command `pytest` in the project folder
