# ruby_python_csv_converter

## Scripts to manipulate CSV data. Written in Ruby and Python.

These scripts currently expect the following column headers (in this order) in the CSV file:

* fid (Warning: There is a hidden `\ufeff` character in this column header in the sample CSV files. I've accounted for it in the scripts, but should be fixed.)
* AREA
* PERIMETER
* ID
* LAND
* NAME
* STATUS
* Rb
* TYPE
* Date
* layer
* path
* GEN
* KREIS_KENN
* Z_KREIS_KE
* KREIS_ID
* RS
* 2_Kreis_Ke
* State
* landkey_Pa
* RB_codes_R
* Longitude
* Latitude

It then returns the a new CSV file that is identical to the input CSV file, except that it adds the following column headers and adds the values to each row:

* Start Date
* End Date
* Date Ranges

Feel free to update as you see fit.

## Input/Output Directories
1. Copy your input CSV file into the 'input_csv_files' directory, make sure it has a '.csv' file name extension
2. Output CSV file will saved in 'output_csv_files' directory with the following file name format: `new_input_csv_file_name.csv`

### To run in Python:
From inside the 'python' directory, run the follow command: `python convert.py input_csv_file_name.csv`

### To run in Ruby:
From inside the 'ruby' directory, run the follow command: `ruby convert.rb input_csv_file_name.csv`
