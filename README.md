# dummy_file_generator
dummy csv or flat text files generator written in Python 3.7

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/rating.svg)

This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).
It consumes arguments defining: 
- projectname ( *based on the projectname, the correct settings from config.json file are loaded ),* 
- filename defining the output file name
- filesize (optional argument) defining the desired size (in kBs) of the output file 
- rowcount (optional argument) defining the desired row count of the output file
- generated files location (optional argument) defining the output files location in case it's different then the default location in /generated_files/..

[How this tool works](#how-this-tool-works)

[How to install and run the program](#how-to-install-and-run-the-program)

[How to setup a new dummy file generator project](#how-to-setup-a-new-dummy-file-generator-project)

[Important notes](#important-notes)


# How this tool works
![alt text][diagram]

[diagram]: https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/diagram.png "How this tool works"


# How to install and run the program
### To install:
`git clone https://www.github.com/datahappy1/dummy_file_generator dummy_file_generator` <br />
<br />
#### On Windows:<br />

You need to set the PYTHONPATH like this:
`set PYTHONPATH=%PYTHONPATH%;C:\dummy_file_generator\`<br />
<br />
A permanent solution is to:<br />
-Go to the Windows menu, right-click on “Computer” and select “Properties”:<br />
-From the computer properties dialog, select “Advanced system settings” on the left:<br />
-From the advanced system settings dialog, choose the “Environment variables” button:<br />
-In the Environment variables dialog, click the “New” button in the top half of the dialog, to make a new user variable:<br />
-Give the variable name as PYTHONPATH and the value is the path to the code directory. Choose OK and OK again to save this variable.<br />
-Now open a cmd Window (Windows key, then type cmd and press Return). Type: `echo %PYTHONPATH%` to confirm the environment variable is correctly set.<br />

*This Pythonpath setup tutorial was taken from https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html
<br />
<br />
#### On Linux:<br />
TODO<br />
<br />

#### Pytest testing:<br />
Pytest (version 3.9.1) unit, integration and performance tests are also a part of this tool.
To make sure you're working with a healthy version, install Pytest running `pip install pytest`<br /> 
( Alternatively you can run the command `pip install -r requirements.txt` to install Pytest )<br />
<br />

To run the tests, just `cd dummy_file_generator` and run the command `pytest`

### To run:<br />
You need to set the required arguments :

projectname -pn <br />
filename -fn <br />

The optional arguments are :

filesize -fs (in kB) <br />
rowcount -rc <br />
generated_files_location -gf <br />

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used

Run these commands to execute:<br />
- with the -fs argument to set the desired filesize of 256 kB :<br />
`cd dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator.py -pn dummy1 -fn dummy1file -fs 256`<br />
- with the -rc argument to set the desired rowcount of 1000 rows :<br />
`cd dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator.py -pn dummy1 -fn dummy1file -rc 1000`<br />


# How to setup a new dummy file generator project

Let's say you need to generate dummy files based on the content of the text files in your "data_files" folder, and these text files are looking like this:

firstnames.txt:  <br />
Frank  <br />
Paul  <br />
John  <br />
Fin  <br />

dates.txt:  <br />
2017-12-30  <br />
2016-01-12  <br />
2015-11-11  <br />

IDs.txt:  <br />
123456789  <br />
987654321  <br />
123  <br />
456  <br />
AA123987  <br />
AB3645  <br />

### - How to generate a .csv file
Let's say you need to generate a dummy .csv file containing 3 columns for Names, Dates and IDs. 
The project element in your config.json would need to be setup like:

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

The output file will be written to a .csv file with the first few rows possibly looking like this:<br />
![alt text][csv]

[csv]: https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/csv_demo.PNG "csv"

### - How to generate a .txt flat file:
Let's say you need to generate a dummy .txt flat file containing 3 columns for Names, Dates and IDs with specific column lengths defined. 
The project element in your config.json would need to be setup like:

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

The output file will be written to a .txt file with the first few rows possibly looking like this:<br />
![alt text][flat]

[flat]: https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/flatfile_demo.PNG "flat"


# Important Notes
- To preserve the existing pytest unit and performance tests, do not remove:
    - test_csv and test_flatfile projects configurations from config.json
    - test.txt file from data_files subfolder
- Whenever you need to add a new source file in the data_file folder, just follow the logic of handling these files in data_files_handler.py and add there your new source file accordingly
- Feel free to contribute to this project
