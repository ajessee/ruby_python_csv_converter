require_relative('csv_obj')
require_relative('add_dates')
require 'csv'
require 'pry-byebug'
require 'humanize'

## Error message helpers
# error message for missing file name
def no_file_name
  puts 'Error: Missing CSV file name.'
  puts 'Use the following format to run this script:'
  puts 'ruby convert.rb input_csv_file_name.csv your_command'
end

# error message for missing command
def no_command
  puts 'Error: Missing command.'
  puts 'Use the following format to run this script:'
  puts 'ruby convert.rb input_csv_file_name.csv your_command'
end

## Main logic
# Throw error if no file name provided
if ARGV.any?
  puts 'Processing data...'
  script_start_time = Time.now
  # get file name
  file_name = ARGV.first
  # additional_args can be used to pass as many additional arguments as you want
  additional_args = ARGV[1..-1]
  # guard clause if command is missing
  if ARGV.length < 2
    no_command
    return
  end
  # command option will always be the first additional argument
  command_option = additional_args[0]
  # array of csv objects, which represent a row in the CSV file 
  csv_objects_array = []
  # get current directory path
  current_dir_path = __dir__
  # relative paths to the input/output CSV file directories
  input_csv_dir = '../input_csv_files'
  output_csv_dir = '../output_csv_files'
  # get path to input csv file
  input_csv_path = File.join(current_dir_path, input_csv_dir, file_name)
  # get path to output csv file
  output_csv_path = File.join(current_dir_path, output_csv_dir, file_name)
  # Get CSV file header row
  headers = CSV.open(input_csv_path, &:readline)

  # read in CSV file
  CSV.foreach(input_csv_path, headers: true) do |row|
    ## 'add_dates' command-specific logic. Remove or replace if needed.
    if command_option == 'add_dates'
      # if name column is blank, skip creating a csv object
      next if test_for_blank_row_data(headers, row, 'NAME', 5)
    end
    # create CSV object with no attributes
    csv_object = CsvObject.new
    row.each do |key, value|
      new_key = humanize_int_in_string(key.downcase.gsub(' ', '_'))
      new_attribute = "@#{new_key}"
      # dynamically add attributes to CSV object using CSV headers
      csv_object.instance_variable_set(new_attribute, value)
      # dynamically add accessor for attribute
      csv_object.class.module_eval { attr_accessor new_key.to_sym }
    end
    # push CSV object into CSV array
    csv_objects_array.push(csv_object)
  end

  ## 'add_dates' command-specific logic. Remove or replace if needed.
  if command_option == 'add_dates'
    # column headers to add to CSV file
    new_column_headers_array = ['Start Date', 'End Date', 'Date Ranges']
    # add new headers to existing headers
    add_column_headers(headers, new_column_headers_array)
    # create date object
    date_object = create_date_object(headers, new_column_headers_array, csv_objects_array)
  end

  # write out new CSV file
  CSV.open(output_csv_path, 'wb') do |csv|
    # write row headers from input CSV file plus the "Start Date", "End Date", "Date Ranges" headers we added using the add_column_headers() function
    csv << headers
    csv_objects_array.each do |csv_object|
      ## 'add_dates' command-specific logic. Remove or replace if needed.
      # add new columns row data
      if command_option == 'add_dates'
        csv_object.start_date, csv_object.end_date, csv_object.date_ranges = create_date_strings(date_object[csv_object.name].uniq)
      end
      # write CSV row using CsvObject instance method that returns array of object properties
      csv << csv_object.to_csv
    end
  end

  script_end_time = Time.now
  puts 'Done.'
  puts "Script took #{(script_end_time - script_start_time).round(2)} seconds to run"

else
  no_file_name
end

