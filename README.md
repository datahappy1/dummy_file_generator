# dummy_file_generator
## version 1.1.17
### Dummy .csv or flat text files generator written in Python 3.7

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/rating.svg)

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/dfg_logo.PNG)


This tool is able to generate dummy csv or flat txt files based on the configuration settings you setup for your project(s).


- [How to install and run the tool as CLI](#how-to-install-and-run-the-tool-as-CLI)

- [How to install and run the tool as an imported package](#how-to-install-and-run-the-tool-as-an-imported-package)

- [How to setup a new dummy file generator project](#how-to-setup-a-new-dummy-file-generator-project)

- [How to add a new source dataset for your project](#How-to-add-a-new-source-dataset-for-your-project)

- [Pytest testing](#Pytest-testing) (for further tool development)

# How to install and run the tool as CLI
One common usage scenario can be load / stress / performance testing of file-processing data tools, allowing you to generate the files needed from a command line.

### To install:
1) `git clone https://github.com/datahappy1/dummy_file_generator c:\dummy_file_generator\`
2) `pip install -r requirements.txt`

>You are strongly encouraged to use the Python virtual environment or Pipenv

### To run:<br />
The CLI tool needs these **MANDATORY** arguments defining: 
- projectname `--projectname` or `-pn` based on the projectname, the dummy file project specific settings from `dummy_file_generator/configs/config.json` file are loaded ,
- absolutepath `--generated_file_path` or `-gp` defining the full output file path to the file you are about to generate

>Provided arguments have higher precedence than fallback values in `settings.py`

The CLI tool can further consume these **OPTIONAL** arguments defining: 
- filesize `--filesize` or `-fs` defining the desired size (in kBs) of the output file 
- rowcount `--rowcount` or `-rc` defining the desired row count of the output file

>Note if you do NOT specify the filesize and do NOT specify the rowcount, the default `row_count` value from
`settings.py` will be used ( or the value you provide in the `default_rowcount` optional argument)

The CLI tool also supports these **OPTIONAL** arguments that can be used to override values in `settings.py`:
- logging_level `--logging_level` or `-ll` defining the Python logging level 
- default_rowcount `--default_rowcount` or `-drc` defining the rowcount fallback value when neither row_count,neither file_size set
- file_encoding `--file_encoding` or `-fen` defining the generated files encoding
- file_line_ending `--file_line_ending` or `-fle` defining the file line ending

These two **OPTIONAL** arguments are typically needed when running the tool as an imported package, but you can use them even with
this tool running as CLI:
- data_files_location `--data_files_location` or `-dfl` defining the path to the source .txt data files 
- config_json_path `--config_json_path` or `-cjp` defining the custom path to your config.json file


#### Example how to run the tool with the -fs argument to set the desired filesize of 256 kB :
1) `cd c:\dummy_file_generator\dummy_file_generator`
2) `python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -gp c:\myfiles\dummy1file.csv -fs 256`

#### Example how to run the tool with the -rc argument to set the desired rowcount of 1000 rows :
1) `cd c:\dummy_file_generator\dummy_file_generator`
2) `python c:\dummy_file_generator\dummy_file_generator\__main__.py -pn dummy1 -gp c:\myfiles\dummy1file.csv -rc 1000`


# How to install and run the tool as an imported package
One common usage scenario can be load / stress / performance testing of file-processing data tools, where you can generate dummy text files during the test fixtures / setup.

### To install:
1) `pip install dummy-file-generator`

### To run:<br />
The dummy file generator imported package needs these **MANDATORY** arguments defining: 
- projectname `--projectname` or `-pn`, based on the projectname, the dummy file specific settings from `config.json` file are loaded,
- generated_file_path `--generated_file_path` or `gp` defining the full output file path to the file you are about to generate

>Provided arguments have higher precedence than fallback values in `settings.py`

The dummy file generator imported package can further consume these **OPTIONAL** arguments defining: 
- filesize `--filesize` or `-fs` defining the desired size (in kBs) of the output file 
- rowcount `--rowcount` or `-rc` defining the desired row count of the output file

>Note if you do NOT specify the filesize and do NOT specify the rowcount, the `DEFAULT_ROW_COUNT` value from
`settings.py` will be used ( you can override the `DEFAULT_ROW_COUNT` value in `settings.py` using the `default_rowcount` optional argument)

- data_files_location `--data_files_location` or `-dfl` defining the path to the source .txt data files 
- config_json_path `--config_json_path` or `-cjp` defining the custom path to your `config.json` file
- logging_level `--logging_level` or `-ll` defining the Python logging level 
- default_rowcount `--default_rowcount` or `-drc` defining the rowcount fallback value when neither row_count,neither file_size set
- file_encoding `--file_encoding` or `-fen` defining the generated files encoding
- file_line_ending `--file_line_ending` or `-fle` defining the file line ending

>In the example below, `project_scope_kwargs` arguments `project_name`, `data_files_location`, `config_json_path` and `default_rowcount` are used
to instantiate a DummyFileGenerator class instance. 
`file_scope_kwargs` arguments `generated_file_path`, `file_size`, `file_encoding` and `file_line_ending` are used to setup the generated file properties.
Once there is a instance of DummyFileGenerator, you can use it to generate as many files as needed while only using
the `write_output_file` method and it's specific `file_scope_kwargs` arguments

#### Example how to run :
```
from dummy_file_generator import DummyFileGenerator as Dfg, DummyFileGeneratorException

logging_level = "INFO"

project_scope_kwargs = {
    "project_name": "dummy1",
    "data_files_location": "c:\\dummy_file_generator\my_data_files",
    "config_json_path": "c:\\dummy_file_generator\my_configs\config.json",
    "default_rowcount": None,
}

try:
    dfg_obj = Dfg(logging_level, **project_scope_kwargs)
except DummyFileGeneratorException as DFG_ERR:
    raise DFG_ERR

file_scope_kwargs = {
    "generated_file_path": "C:\dfg_refact_package_test\\bin\\file1.csv",
    "file_size": 1024,
    #"row_count": None,
    "file_encoding": "utf8",
    "file_line_ending": "\n",
}

try:
    dfg_obj.write_output_file(**file_scope_kwargs)
except DummyFileGeneratorException as DFG_ERR:
    raise DFG_ERR
```

# How to setup a new dummy file generator project
You need to generate dummy files based on the content of the text files in your `data_files` folder, and these source text files need to have this plain text format:

![](https://github.com/datahappy1/dummy_file_generator/blob/master/docs/img/first_names.PNG)

This tool picks random item from each of the files configured for your project in config.json and uses these values to populate the data for "columns" for each written row. 

### - How to generate a .csv file
If you need to generate a dummy .csv file containing 3 columns for Names, Dates and IDs, 
the project JSON object in your config.json would need to be setup like:

    {
      "project_name":"dummy1",
      "file_type":"csv",
      "header":true,
      "csv_value_separator": ",",
      "csv_quoting": "ALL",
      "csv_quote_char": "\n"",
      "csv_escape_char": "\\",
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
If you need to generate a dummy .txt flat file containing 3 columns for Names, Dates and IDs with specific column lengths defined, 
the "project" JSON object in your config.json would need to be setup like:

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
**The filename needs to correspond with the datafile value in your config.json file.**

If running as a standalone CLI tool, the `data_files` folder is located here:
`dummy_file_generator/data_files`

When running as an imported package, the `data_files` folder is where ever you specify it to be
using the argument `data_files_location`.

Now you can use this new data file in your project setup in `config.json` file. 

# Pytest testing
Pytest unit and performance tests are also a part of this repository.
You can install Pytest using `pip install pytest`

### To run tests:
1) `cd c:\dummy_file_generator\dummy_file_generator`
2) `python -m pytest c:\dummy_file_generator\tests`
( In case when running from IDE, make sure the current working dir is set to `c:\\dummy_file_generator`)
