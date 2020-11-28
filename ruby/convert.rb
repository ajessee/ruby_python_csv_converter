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

# convert integers in string to humanized form.
# Needed for converting string to symbol since in Ruby, you can't have an int at the beginning of a symbol
def humanize_int_in_string(input_string)
  int_index = input_string.index(/\d+/)
  if int_index
    int_string = input_string[int_index]
    int_humanized = int_string.to_i.humanize
    input_string.gsub!(int_string, int_humanized)
  end
  input_string
end

## Command switch logic
def command_logic(command, stage, args)
  args_array = [command, stage, args]
  case args_array
  when AddDates
    return_object = AddDates.matcher(args_array)
  end
  return_object
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
    ## Command logic, 'read' stage.
    # For 'add_dates', will return true if name column is blank, skipping iteration.
    next if command_logic(
      command_option,
      'read',
      {
        headers: headers,
        row: row
      }
    )

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

  ## Command logic, 'setup' stage.
  # For 'add_dates', will add new headers and create date object which will be used in write stage.
  # Date object will be stored in AddDates class variable.
  command_logic(
    command_option,
    'setup',
    {
      headers: headers,
      csv_objects_array: csv_objects_array
    }
  )

  # write out new CSV file
  CSV.open(output_csv_path, 'wb') do |csv|
    # write original row headers from input CSV file
    csv << headers
    csv_objects_array.each do |csv_object|
      ## Command logic, 'write' stage
      ## For 'add_dates', will add new columns "Start Date", "End Date", "Date Ranges" row data to CSV object
      command_logic(
        command_option,
        'write',
        {
          csv_object: csv_object
        }
      )
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
