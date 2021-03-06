import csv
import sys
import time
import os
from csv_obj import CsvObject
# add 'breakpoint()' in code for debugging
import pdb
# import functions for date adding command
from add_dates import AddDates

# Error message helpers
# error message for missing file name
def no_file_name():
    print('Error: Missing CSV file name.')
    print('Use the following format to run this script:')
    print('python convert.py input_csv_file_name.csv your_command')

# error message for missing command
def no_command():
    print('Error: Missing command.')
    print('Use the following format to run this script:')
    print('python convert.py input_csv_file_name.csv your_command')

# Command switch logic
def command_logic(command, stage, args):
    args_array = [command, stage, args]
    if command == 'add_dates':
        return_object = AddDates.matcher(AddDates, args_array)
    # to add new commands, add below
    # elif command == 'add_new_command_here':
    #     return_object = YourClass.matcher(YourClass, args_array)
    return return_object


# Main logic
# Throw error if no file name provided
if (len(sys.argv) > 1):
    print('Processing data...')
    script_start_time = time.time()
    # get file name
    file_name = sys.argv[1]
    # guard clause if command is missing
    if len(sys.argv) < 3:
        no_command()
        sys.exit()
    # additional_args can be used to pass as many additional arguments as you want
    additional_args = sys.argv[2:]
    # command option will always be the first additional argument
    command_option = additional_args[0]
    grouping_column = additional_args[1] if len(additional_args) > 1 else None
    grouping_index = 0
    # array of csv objects, each represent a row in the CSV file
    csv_objects_array = []
    # get current directory path
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    # relative paths to the input/output CSV file directories
    input_csv_dir = '../input_csv_files'
    output_csv_dir = '../output_csv_files'
    # get path to input csv file
    input_csv_path = os.path.join(current_dir_path, input_csv_dir, file_name)
    # get path to output csv file
    output_csv_path = os.path.join(current_dir_path, output_csv_dir, file_name)

    # read in CSV file
    # utf-8-sig encoding will remove all BOMs (Byte Order Marks)
    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        # get array of all rows
        reader = csv.reader(f)
        # Get CSV file header row, remove from reader array
        headers = next(reader, None)
        if grouping_column:
            grouping_index = headers.index(grouping_column)
        else:
            grouping_column = 'NAME'
            grouping_index = headers.index(grouping_column)

        for row in reader:
            # Command logic, 'read' stage.
            # For 'add_dates', will return true if name column is blank, skipping iteration.
            if command_logic(
                command_option,
                'read',
                {
                    "headers": headers,
                    "row": row,
                    "grouping_column": grouping_column,
                    "grouping_index": grouping_index
                }
            ):
                continue
            # create CSV object with no attributes
            csv_object = CsvObject()
            # dynamically add attributes to CSV object using CSV headers
            for idx, header in enumerate(headers):
                setattr(csv_object, header.replace(" ", "_").lower(), row[idx])
            # push CSV object into CSV array
            csv_objects_array.append(csv_object)

    # Command logic, 'setup' stage.
    # For 'add_dates', will add new headers and create date object which will be used in write stage.
    # Date object will be stored in AddDates class variable.
    command_logic(
        command_option,
        'setup',
        {
            "headers": headers,
            "csv_objects_array": csv_objects_array
        }
    )

    # write out new CSV file
    with open(output_csv_path, 'w') as new_file:
        file_writer = csv.writer(
            new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write row headers from input CSV file plus the start date, end date, date ranges headers we added using the add_column_headers() function
        file_writer.writerow(headers)

        for csv_object in csv_objects_array:
            # Command logic, 'write' stage
            # For 'add_dates', will add new columns "Start Date", "End Date", "Date Ranges" row data to CSV object
            command_logic(
                command_option,
                'write',
                {
                    "csv_object": csv_object,
                    "headers": headers
                }
            )
            # write CSV row using csvObject to_csv() instance method that returns array of object attributes
            file_writer.writerow(csv_object.to_csv())

    script_end_time = time.time()
    print('Done.')
    print(
        f'Script took {str(round((script_end_time - script_start_time), 2))} seconds to run')

else:
    no_file_name()
