# dummy_file_generator
## Dummy .csv or .flat files generator in Python 3

This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).
It consumes arguments to define #####projectname ( based on the projectname, the correct settings from config.json are loaded ) , #####filename defining the output file name, #####filesize to define the needed file size of the output file and an optional argument defining the output files location in case it's different then the default location in /generated_files/..

### How to setup a project in this tool

Let's assume your data_files txt files look like these 3 below:

firstnames.txt:  <br />
Frank  <br />
Paul  <br />
John  <br />
Fin  <br />

dates.txt:  <br />
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



#### output is a .csv file
Let's say you need to generate a dummy .csv file containing 3 columns for Names, Dates and IDs. 
The project element in your config.json would look like:

    {
      "project_name":"dummy1",
      "file_type":"csv",
      "file_extension":"csv",
      "header":true,
      "columns":[
        {
          "column_name":"Name",
          "datafile":"firstnames.txt"
        },
        {
          "column_name":"Date",
          "datafile":"dates.txt"
        },
        {
          "column_name":"ID",
          "datafile":"IDs.txt"
        }      
      ]
    }


The output file will be written to a .csv file looking like this:

Name,Date,ID<br />
Frank,2017-12-30,123456789<br />
Paul,2016-01-12,987654321<br />
John,2015-11-11,123<br />
Frank,2008-01-03,456<br />
Paul,2017-12-30,AA123987<br />
John,2016-01-12,AB3645<br />



#### output is a .txt flat file
Let's say you need to generate a dummy .txt flat file containing 3 columns for Names, Dates and IDs with specific column lengths defined. 
The project element in your config.json would look like:

    {
      "project_name":"dummy1",
      "file_type":"flat",
      "file_extension":"txt",
      "header":true,
      "columns":[
        {
          "column_name":"Name",
          "column_len":6,
          "datafile":"firstnames.txt"
        },
        {
          "column_name":"Date",
          "column_len":10,
          "datafile":"dates.txt"
        },
        {
          "column_name":"ID",
          "column_len":9,
          "datafile":"IDs.txt"
        }      
      ]
    }


The output file will be written to a .txt file looking like this:

| Name   | Date       | ID        | 
| :----- | :--------- | :-------- | 
| Frank  | 2017-12-30 | 123456789 | 
| Paul   | 2016-01-12 | 987654321 | 
| John   | 2015-11-11 | 123       | 
| Frank  | 2008-01-03 | 456       | 
| Paul   | 2017-12-30 | AA123987  | 
| John   | 2016-01-12 | AB3645    | 


### How to run this tool
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
