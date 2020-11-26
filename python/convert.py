# To run this script, enter the following command in the command line (replace input_csv_file_name with your file's name):
# python convert.py input_csv_file_name.csv add_dates
# Make sure your input CSV file is in the 'input_csv_files/' directory
import csv
import sys
import pdb
import os
# import functions from add_dates.py
from add_dates import create_date_object, add_column_headers, set_date_attributes_in_csv_obj, test_for_blank_row_data, create_date_strings
from csv_obj import CsvObject

# will only run if you provide file name in command line
if (len(sys.argv) > 1):

  file_name = sys.argv[1]
  # additional_args can be used to pass as many additional arguments as you want
  additional_args = sys.argv[2:]
  # command option will always be the first additional argument
  command_option = additional_args[0]
  # array of csv objects, which represent a row in the CSV file
  csv_objects_array = []
  # get current directory
  current_dir_path = os.path.dirname(os.path.realpath(__file__))
  # relative paths to the input/output CSV file directories
  input_csv_dir = '../input_csv_files'
  output_csv_dir = '../output_csv_files'
  # get path to input csv file
  input_csv_path = os.path.join(current_dir_path, input_csv_dir, file_name)
  # get path to output csv file
  output_csv_path = os.path.join(current_dir_path, output_csv_dir, file_name)
  # to extend this script, add other functions into another python file in this directory, and then import at the top of this file.
  # then, nest any logic in an 'if' condition block. Example:
  # if command_option == "your_command":
  #   your_logic_here

  # utf-8-sig encoding will remove all BOMs (Byte Order Marks)
  with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    # Get CSV file header row
    headers = next(reader, None)

    for row in reader:
      if command_option == "add_dates":
        # don't create csv_object if row data for 'Name' column is blank
        if test_for_blank_row_data(headers, row, 'Name', 5):
          continue
      # create csv object and append to array
      csv_object = CsvObject()
      for idx, header in enumerate(headers):
        setattr(csv_object, header.replace(" ", "_").lower(), row[idx])
      csv_objects_array.append(csv_object)

  # logic specific to 'add_dates' command
  if command_option == "add_dates":
    # column headers to add to CSV file
    new_column_headers_array = ["Start Date", "End Date", "Date Ranges"]
    # add new headers to existing headers
    add_column_headers(headers, new_column_headers_array)
    # create date object
    date_object = create_date_object(headers, new_column_headers_array, csv_objects_array)

  with open(output_csv_path, 'w') as new_file:
    file_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write original row headers plus the start date, end date, date ranges headers we added
    file_writer.writerow(headers)

    for csv_object in csv_objects_array:
      # only add new column data command is add_dates
      if command_option == "add_dates":
        set_date_attributes_in_csv_obj(csv_object, date_object, headers)

      # write CSV row using csvObject instance method that returns array of object properties
      file_writer.writerow(csv_object.to_csv())
