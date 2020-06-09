# dummy_file_generator
## version 1.0.7
a dummy csv or flat text files generator written in Python 3.7

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/rating.svg)

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/dfg_logo.PNG)


This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).


[How to install and run the tool as CLI](#how-to-install-and-run-the-tool-as-CLI)

[How to install and run the tool as an imported package](#how-to-install-and-run-the-tool-as-an-imported-package)

[How to setup a new dummy file generator project](#how-to-setup-a-new-dummy-file-generator-project)

[How to add a new source dataset for your project](#How-to-add-a-new-source-dataset-for-your-project)

[Pytest testing](#Pytest-testing)

# How to install and run the tool as CLI
One common usage scenario can be load / stress / performance testing of file-processing data tools, allowing you to generate the files needed from a command line.

### To install:
`git clone https://github.com/datahappy1/dummy_file_generator c:\dummy_file_generator\`<br />
`pip install -r requirements.txt`

*You are strongly encouraged to use the Python virtual environment

### To run:<br />
The CLI tool needs these mandatory arguments defining: 
- projectname `--projectname` or `-pn` (mandatory argument, *based on the projectname, the dummy file specific settings from /configurables/config.json file are loaded ),* 
- absolutepath `--absolutepath` or `-ap` (mandatory argument) defining the full output file path to the file you wish to generate

The CLI tool can consume these optional arguments defining: 
- filesize `--filesize` or `-fs` (optional argument) defining the desired size (in kBs) of the output file 
- rowcount `--rowcount` or `-rc` (optional argument) defining the desired row count of the output file

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used ( or the value you provide in the `default_rowcount` optional argument)

*these 5 optional arguments can be used to override values in `configurables/settings.py`:
- logging_level `--logging_level` or `-ll` (optional argument) defining the Python logging level 
- default_rowcount `--default_rowcount` or `-drc` (optional argument) defining the rowcount fallback value when neither row_count,neither file_size set
- file_encoding `--file_encoding` or `-fen` (optional argument) defining the generated files encoding
- file_line_ending `--file_line_ending` or `-fle` (optional argument) defining the file line ending
- csv_value_separator `--csv_value_separator` or `-cvs` (optional argument) defining the .csv file value separator

*these arguments are typically needed when running the tool as an importable library, but you can
use them to change the location of the source data files and the config json with the project setup even with
this tool running as CLI:
- data_files_location `--data_files_location` or `-dfl` (optional argument) defining the path to the source .txt data files 
- config_json_path `--config_json_path` or `-cjp` (optional argument) defining the custom path to your config.json file

Example how to run :<br />
- with the -fs argument to set the desired filesize of 256 kB :<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -fs 256`<br />
- with the -rc argument to set the desired rowcount of 1000 rows :<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -ap c:\myfiles\dummy1file.csv -rc 1000`<br />


# Pytest testing
Pytest unit and performance tests are also a part of this tool.
You can install Pytest with `pip install pytest`<br /> 
To run tests:<br />
`cd c:\dummy_file_generator\dummy_file_generator`<br />
`pytest`<br />


# How to install and run the tool as an imported package
One common usage scenario can be load / stress / performance testing of file-processing data tools, where you can now generate dummy text files during the test fixtures / setup.

### To install:
`pip install dummy-file-generator`<br />

### To run:<br />
The dummy file generator imported package needs these mandatory arguments defining: 
- projectname `--projectname` or `-pn` (mandatory argument, *based on the projectname, the dummy file specific settings from config.json file are loaded ),* 
- absolutepath `--absolutepath` or `-ap` (mandatory argument) defining the full output file path to the file you wish to generate

The dummy file generator imported package can consume these optional arguments defining: 
- filesize `--filesize` or `-fs` (optional argument) defining the desired size (in kBs) of the output file 
- rowcount `--rowcount` or `-rc` (optional argument) defining the desired row count of the output file

*Note if you do NOT specify the filesize and do NOT specify the rowcount, the default row_count value ( set to 100 ) from
settings.py will be used ( or the value you provide in the `default_rowcount` optional argument)

- data_files_location `--data_files_location` or `-dfl` (optional argument) defining the path to the source .txt data files 
- config_json_path `--config_json_path` or `-cjp` (optional argument) defining the custom path to your config.json file
- logging_level `--logging_level` or `-ll` (optional argument) defining the Python logging level 
- default_rowcount `--default_rowcount` or `-drc` (optional argument) defining the rowcount fallback value when neither row_count,neither file_size set
- file_encoding `--file_encoding` or `-fen` (optional argument) defining the generated files encoding
- file_line_ending `--file_line_ending` or `-fle` (optional argument) defining the file line ending
- csv_value_separator `--csv_value_separator` or `-cvs` (optional argument) defining the .csv file value separator


Example how to run :<br /><br />
```
from dummy_file_generator import DummyFileGenerator as DFG, DummyFileGeneratorException

def generate_dummy_file(project_name, absolute_path, file_size,
                        data_files_location, config_json_path):
    kwargs = {"project_name": project_name, 
              "absolute_path": absolute_path,
              "file_size": file_size,
              "logging_level": "INFO",
              "data_files_location": data_files_location,
              "config_json_path": config_json_path,
              "file_encoding": "utf8",
              "csv_value_separator": "%",
              "file_line_ending": "\n"
              }

    obj = DFG(**kwargs)
    try:
        DFG.generate_file(obj)
    except DummyFileGeneratorException as DFG_ERR:
        raise(DFG_ERR)
        
    
generate_dummy_file(project_name="dummy1",
                    absolute_path="c:\myfiles\dummy1.csv", 
                    file_size=1024,
                    data_files_location="c:\\dummy_file_generator\dummy_file_generator\data_files",
                    config_json_path="c:\\dummy_file_generator\dummy_file_generator\configurables\config.json"
                    )
```

# How to setup a new dummy file generator project
You need to generate dummy files based on the content of the text files in your "data_files" folder, and these source text files need to be setup for instance like this:

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/first_names.PNG)

This tool picks random item from each of the files configured for your project in config.json and uses these values to populate the data for "columns" for each written row. 

### - How to generate a .csv file
Let's say you need to generate a dummy .csv file containing 3 columns for Names, Dates and IDs. 
The "project" JSON object in your config.json would need to be setup like:

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
The "project" JSON object in your config.json would need to be setup like:

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
Whenever you need to add a new source .txt file in the data_files folder, just add it to your `data_files` folder. 
If running as a standalone CLI tool, the data_files folder is located here:
`dummy_file_generator/data_files`

When running as an imported package, the data_files folder is whereever you set it in
the argument data_files_location.
Now you can use this new data file in your project setup in `config.json` file. 
