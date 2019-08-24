# dummy_file_generator
dummy csv or flat text files generator written in Python 3.7

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/rating.svg)

This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).
It consumes arguments defining: 
- projectname ( *based on the projectname, the specific settings from config.json file are loaded ),* 
- absolutepath defining the full output file path to the file you wish to generate
- filesize (optional argument) defining the desired size (in kBs) of the output file 
- rowcount (optional argument) defining the desired row count of the output file

[How to install and run the program](#how-to-install-and-run-the-program)

[How to setup a new dummy file generator project](#how-to-setup-a-new-dummy-file-generator-project)

[Important notes](#important-notes)


# How to install and run the program
### To install:
`pip install dummy_file_generator`

#### Pytest testing:<br />
Pytest unit and performance tests are also a part of this tool.
Install Pytest with `pip install pytest`<br /> 

### To run:<br />
You need to set the required arguments :

projectname -pn <br />
absolutepath -ap <br />

The optional arguments are :

filesize -fs (in kB) <br />
rowcount -rc <br />

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used

Run these commands to execute:<br />
- with the -fs argument to set the desired filesize of 256 kB :<br />
`python c:\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -fs 256`<br />
- with the -rc argument to set the desired rowcount of 1000 rows :<br />
`cd dummy_file_generator`<br />
`python c:\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -rc 1000`<br />

*You are strongly encouraged to use Python virtual environment, for example on Windows:<br />
1: install virtualenv: `pip install virtualenv`<br />
2: switch dir context: `cd c:\dummy_file_generator`<br />
3: spin up the virtual env: `python -m virtualenv dfg`<br />
4: switch dir context and activate: `cd dfg/Scripts` and run `activate.bat`<br />
5: install the dummy_file_generator tool from pip: `python -m pip install --index-url https://pypi.org/simple/ --no-deps dummy_file_generator`<br />
6: run pytest: `(dfg) c:\dummy_file_generator\dfg\Lib\site-packages\dummy_file_generator>pytest`<br />
7: run the tool to generate a dummy file: `(dfg) c:\dummy_file_generator\dfg\Lib\site-packages\dummy_file_generator>__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -fs 256`<br />
8: once finished, deactivate the virtual env: `deactivate.bat`<br />

# How to setup a new dummy file generator project

Let's say you need to generate dummy files based on the content of the text files in your "data_files" folder, and these text files are looking like this:

### - How to generate a .csv file
Let's say you need to generate a dummy .csv file containing 3 columns for Names, Dates and IDs. 
The project element in your config.json would need to be setup like:

    {
      "project_name":"dummy1",
      "file_type":"csv",
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

### - How to generate a .txt flat file:
Let's say you need to generate a dummy .txt flat file containing 3 columns for Names, Dates and IDs with specific column lengths defined. 
The project element in your config.json would need to be setup like:

    {
      "project_name":"dummy1",
      "file_type":"flat",
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

### - How to add a new source dataset for your project:
Whenever you need to add a new source text file in the data_files folder, just follow the logic of handling these files in `data_files_handler.py`. 
Let's say you need to generate dummy file containing also Social Security Number SSN. 
Add into `Class DataSets` a row like this: `SSN = load_file_to_list('SSN.txt')`
Now you can use SSNs in your project setup in `config.json` file. 

# Important Notes
- To preserve the existing pytest unit and performance tests, do not remove:
    - `test_csv` and `test_flatfile` projects configurations from `config.json`
    - `test.txt` file from `data_files` subfolder
- Feel free to contribute to this project
