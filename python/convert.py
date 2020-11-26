import csv
import sys
import os
from csv_obj import CsvObject
# add 'breakpoint()' in code for debugging
import pdb
# import functions for date adding command
from add_dates import create_date_object, add_column_headers, set_date_attributes_in_csv_obj, test_for_blank_row_data, create_date_strings

# to extend this script, add other functions into another python file in this directory, and then import as above.
# then, nest command-specific logic in an 'if' condition block. Example:
# if command_option == "your_command":
#   invoke_your_function()

# will only run if you provide file name in command line
if (len(sys.argv) > 1):

  file_name = sys.argv[1]
  # additional_args can be used to pass as many additional arguments as you want
  additional_args = sys.argv[2:]
  # command option will always be the first additional argument
  command_option = additional_args[0]
  # array of csv objects, each represent a row in the CSV file
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

  # utf-8-sig encoding will remove all BOMs (Byte Order Marks)
  with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
    # get array of all rows
    reader = csv.reader(f)
    # Get CSV file header row, remove from reader array
    headers = next(reader, None)

    for row in reader:
      ## 'add_dates' command-specific logic. Remove or replace if needed.
      if command_option == "add_dates":
        # don't create CSV object if row data for 'Name' column is blank
        if test_for_blank_row_data(headers, row, 'Name', 5):
          continue
      # create CSV object with no attributes
      csv_object = CsvObject()
      # dynamically add attributes to CSV object using CSV headers
      for idx, header in enumerate(headers):
        setattr(csv_object, header.replace(" ", "_").lower(), row[idx])
      # push CSV object into CSV array
      csv_objects_array.append(csv_object)

  ## 'add_dates' command-specific logic. Remove or replace if needed.
  if command_option == "add_dates":
    # column headers to add to CSV file
    new_column_headers_array = ["Start Date", "End Date", "Date Ranges"]
    # add new headers to existing headers
    add_column_headers(headers, new_column_headers_array)
    # create date object
    date_object = create_date_object(headers, new_column_headers_array, csv_objects_array)

  with open(output_csv_path, 'w') as new_file:
    file_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write row headers from input CSV file plus the start date, end date, date ranges headers we added using the add_column_headers() function
    file_writer.writerow(headers)

    for csv_object in csv_objects_array:
      ## 'add_dates' command-specific logic. Remove or replace if needed.
      # add new columns row data
      if command_option == "add_dates":
        set_date_attributes_in_csv_obj(csv_object, date_object, headers)

      # write CSV row using csvObject to_csv() instance method that returns array of object attributes
      file_writer.writerow(csv_object.to_csv())
