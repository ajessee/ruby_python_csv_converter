# ruby_python_csv_converter

## Scripts to manipulate CSV data. Written in Ruby and Python.

### Input/Output Directories
1. Copy your input CSV file into the 'input_csv_files' directory, make sure it has a '.csv' file name extension
2. Output CSV file will saved in 'output_csv_files' directory with the same name as the input file.

### To run in Python:
From inside the 'python' directory, run the following command:
* `python convert.py input_csv_file_name.csv your_command`
**Don't forget to:**
* replace 'input_csv_file_name.csv' with your file's name
* replace your_command.csv with the command you want to run

### To run in Ruby:
From inside the 'ruby' directory, run the following command: 
* `ruby convert.rb input_csv_file_name.csv`
**Don't forget to:**
* replace 'input_csv_file_name.csv' with your file's name

## Currently supported commands:
* `add_dates`
  - If CSV file has a `Date` column, it will collect all dates (years in `2000` format) from each row that shares the same name from the `Name` column, and then add a `Start Date` column that contains the earliest year found in `Name` array of rows, an `End Date` column that contains the latest year found in `Name` array of rows, and add a `Date Range` column that shows any gaps in years.
