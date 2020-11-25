# To run this file, enter the following command in the command line:
# ruby convert.rb input_csv_file_name.csv
# Make sure your input CSV file is in the 'input_csv_files/' directory
require_relative('geo_obj')
require 'csv'
require 'pry-byebug'

# will only run if you provide file name in command line
if ARGV.any?
  file_name = ARGV.first
  # options aren't being used now, but you can extend this in the future if you want
  options = ARGV[1..-1]
  # array of geo objects, which represent a row in the CSV file 
  geo_objects_array = []
  # get current directory
  current_dir_path = __dir__
  # relative paths to the input/output CSV file directories
  input_csv_dir = '../input_csv_files'
  output_csv_dir = '../output_csv_files'
  # create output file name
  output_file_name = 'new_' + file_name
  # get path to input csv file
  input_csv_path = File.join(current_dir_path, input_csv_dir, file_name)
  # get path to output csv file
  output_csv_path = File.join(current_dir_path, output_csv_dir, output_file_name)
  # Get CSV file header row
  incoming_csv_headers = CSV.open(input_csv_path, &:readline)
  # Append the new column names to the end of existing header array
  incoming_csv_headers.push("Start Date")
  incoming_csv_headers.push("End Date")
  incoming_csv_headers.push("Date Ranges")


  # create array of geo objects
  CSV.foreach(input_csv_path, headers: true) do |row|
    row_hash = row.to_h
    new_hash = {}
    row_hash.keys.each_with_index do |key, index|
      new_key = key.downcase.to_sym
      # there is a \ufeff character in the fid column name ('\ufefffid'), so we replace it with just 'fid'. You should probably reformat your spreadsheet column names
      new_key = :f_id if index == 0
      # change key, Ruby doesn't like numbers at the begining of a symbol
      new_key = :two_kreis_ke if key == "2_Kreis_Ke"
      new_hash[new_key] = row_hash[key] if row_hash[key]        
    end
    # create geo object and push into array
    # if name column is blank, skip creating a geo object 
    geo_objects_array << GeoObject.new(new_hash) if new_hash[:name]
  end

  # blank object store key/value pair of geo region name and dates array. Example:
  # {
  #   AACHEN: [1820, 1836, 1837, 1838....]
  # }
  date_object = {}

  geo_objects_array.each do |geo_object|
    # if geo region name is already key in array, append date into value array
    if date_object[geo_object.name]
      date_object[geo_object.name].push(geo_object.date.to_i)
    # else, create key and array with first date value
    else
      date_object[geo_object.name] = [geo_object.date.to_i]
    end
  end

  # helper function to create string of date ranges
  def create_date_strings(array_of_dates)
    start_date = ""
    end_date = ""
    range_string = ""
    array_of_dates.sort.each_with_index do |date, idx|
      # first date in array
      if idx == 0
        range_string += date.to_s
        start_date = date.to_s
        end_date = date.to_s if array_of_dates.length == idx + 1
      # last date in array
      elsif idx + 1 == array_of_dates.length
        delimiter = ""
        if date - 1 == array_of_dates[idx - 1]
          delimiter += "-"
        else
          delimiter += ", "
        end
        range_string += "#{delimiter}#{date}"
        end_date = date.to_s
      # all dates in between
      else
        # date +1 equals next date in array and date -1 equals last date in array. ([1910,1911,1912] we are looking at 1912)
        if date + 1 == array_of_dates[idx + 1] && date - 1 == array_of_dates[idx - 1]
          next
        # date +1 equals next date in array and date -1 does not equal last date in array. ([1905,1911,1912] we are looking at 1911)
        elsif date + 1 == array_of_dates[idx + 1] && date - 1 != array_of_dates[idx - 1]
          range_string += ", #{date}"
        # date +1 does not equal next date in array and date -1 does equal last date in array. ([1910,1911,1920] we are looking at 1911)
        elsif date + 1 != array_of_dates[idx + 1] && date - 1 == array_of_dates[idx - 1]
          range_string += "-#{date}"
        # date +1 does not equal next date in array and date -1 does not equal last date in array. ([1910,1915,1920] we are looking at 1915)
        elsif date + 1 != array_of_dates[idx + 1] && date - 1 != array_of_dates[idx - 1]
          range_string += ", #{date}"
        end
      end
    end
    # return array with start date, end date, range string
    [start_date, end_date, range_string]
  end

  CSV.open(output_csv_path, 'wb') do |csv|
    # write original row headers plus the start date, end date, date ranges headers we added
    csv << incoming_csv_headers
    geo_objects_array.each do |geo_object|
      geo_object.start_date, geo_object.end_date, geo_object.date_ranges = create_date_strings(date_object[geo_object.name].uniq)
      # write CSV row using GeoObject instance method that returns array of object properties
      csv << geo_object.to_csv
    end
  end

end



