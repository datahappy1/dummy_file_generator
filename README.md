# dummy_file_generator
## version 1.0.2
a dummy csv or flat text files generator written in Python 3.7

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/rating.svg)

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/dfg_logo.PNG)


This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).
It consumes arguments defining: 
- projectname (mandatory argument, *based on the projectname, the specific settings from config.json file are loaded ),* 
- absolutepath (mandatory argument) defining the full output file path to the file you wish to generate
- filesize (optional argument) defining the desired size (in kBs) of the output file 
- rowcount (optional argument) defining the desired row count of the output file
- logging_level (optional argument) defining the Python logging level 

- default_rowcount (optional argument) defining the rowcount fallback value when neither row_count,neither file_size set
- file_encoding (optional argument) defining the generated files encoding
- file_line_ending (optional argument) defining the file line ending
- csv_value_separator (optional argument) defining the .csv file value separator

these arguments are needed when running as an importable library:
- data_files_location (optional argument) defining the path to the source .txt data files 
- config_json_path (optional argument) defining the custom path to your config.json file



[How to install and run the program as CLI](#how-to-install-and-run-the-program-as-CLI)

[How to install and run the program as a importable library](#how-to-install-and-run-the-program-as-a-importable-library)

[How to setup a new dummy file generator project](#how-to-setup-a-new-dummy-file-generator-project)

[How to add a new source dataset for your project](#How-to-add-a-new-source-dataset-for-your-project)

[Pytest testing](#Pytest-testing)


# How to install and run the program as CLI
### To install:
`git clone https://github.com/datahappy1/dummy_file_generator c:\dummy_file_generator\`<br />

`cd c:\dummy_file_generator\dummy_file_generator`

`python.exe __main__.py -pn my_project -ap c:\dummy1file.txt -rc 256`

### To run:<br />
You need to set the required arguments :
projectname `-pn` <br />
absolutepath `-ap` <br />

The optional arguments are :
filesize `-fs` (in kB) <br />
rowcount `-rc` <br />

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used ( or the value you provide in the `default_rowcount` optional argument)

Run these commands to execute:<br />
- with the -fs argument to set the desired filesize of 256 kB :<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -fs 256`<br />
- with the -rc argument to set the desired rowcount of 1000 rows :<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -rc 1000`<br />

*You are strongly encouraged to use Python virtual environment

# How to install and run the program as a importable library
### To install:
`pip install -i https://test.pypi.org/simple/ dummy-file-generator`<br />

### To run:<br />
You need to set these arguments as an Python dictionary:
    kwargs = {"project_name": "dummy1", "absolute_path": "C:\\scrap_files\dummy1.csv",
              "file_size": 1024,
              "logging_level": "DEBUG",
              "data_files_location": "c:\\dummy_file_generator\dummy_file_generator\data_files",
              "config_json_path": "c:\\dummy_file_generator\dummy_file_generator\configurables\config.json",
              }

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used ( or the value you provide in the `default_rowcount` optional argument)

Run from within a function in your project for example:<br />
```
from dummy_file_generator import DummyFileGenerator as DFG

def generate_dummy_file():
    kwargs = {"project_name": "dummy1", "absolute_path": "C:\\x\dfxx.csv",
              "file_size": 1024,
              "logging_level": "DEBUG",
              "data_files_location": "c:\\dummy_file_generator\dummy_file_generator\data_files",
              "config_json_path": "c:\\dummy_file_generator\dummy_file_generator\configurables\config.json",
              }

    obj = DFG(**kwargs)
    DFG.executor(obj)

generate_dummy_file()

```

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

# How to add a new source dataset for your project
Whenever you need to add a new source .txt file in the data_files folder, just add it to the `data_files` folder. 
Now you can use this new data file in your project setup in `config.json` file. 

# Pytest testing
Pytest unit and performance tests are also a part of this tool.
You can install Pytest with `pip install pytest`<br /> 
To run tests:<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`pytest`<br />