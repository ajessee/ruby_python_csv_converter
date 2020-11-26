## create date object to hold date info for geographic region
# object will store key/value pair of CSV region name and dates array. Example:
# {
#   AACHEN: [1820, 1836, 1837, 1838....]
# }
def create_date_object(headers, new_column_headers_array, csv_objects_array)
  return unless headers.include?('Date')

  date_object = {}
  csv_objects_array.each do |csv_object|
    # dynamically add new column header attributes and attribute values to CSV object
    new_column_headers_array.each do |new_column_header|
      new_accessor_key = humanize_int_in_string(new_column_header.downcase.gsub(' ', '_'))
      # dynamically add accessor for attribute
      csv_object.class.module_eval { attr_accessor new_accessor_key.to_sym }
    end
    # if geo region name is already key in array, append date into value array
    if date_object[csv_object.name]
      date_object[csv_object.name].push(csv_object.date.to_i)
    # else, create key and array with first date value
    else
      date_object[csv_object.name] = [csv_object.date.to_i]
    end
  end
  date_object
end

# convert integers in string to humanized form. Needed for converting string to symbol since in Ruby, you can't have an int at the beginning of a symbol
def humanize_int_in_string(input_string)
  int_index = input_string.index(/\d+/)
  if int_index
    int_string = input_string[int_index]
    int_humanized = int_string.to_i.humanize
    input_string.gsub!(int_string, int_humanized)
  end
  input_string
end

## add new column headers to existing header row from CSV file
def add_column_headers(headers, new_column_headers_array)
  new_column_headers_array.each do |column_header|
    headers.append(column_header)
  end
end

## set new attributes in CSV object. In this case, we are adding "Start Date", "End Date", "Date Ranges"
def set_date_attributes_in_csv_obj(csv_object, date_object, headers)
  return unless headers.include?('Date') && !csv_object.name.nil?

  # set start date, end date, date ranges attributes in CSV object from return value of create_date_strings()
  geo_object.start_date, geo_object.end_date, geo_object.date_ranges = create_date_strings(date_object[geo_object.name].uniq.sort)
end

## test if row data for column is blank
def test_for_blank_row_data(headers, row, header_name, index)
  if headers[index] == header_name && row[index].nil?
    true
  else
    false
  end
end

## create string of date ranges
def create_date_strings(array_of_dates)
  start_date = ""
  end_date = ""
  range_string = ""
  array_of_dates.sort.each_with_index do |date, idx|
    # first date in array
    if idx.zero?
      range_string += date.to_s
      start_date = date.to_s
      end_date = date.to_s if array_of_dates.length == idx + 1
    # last date in array
    elsif idx + 1 == array_of_dates.length
      delimiter = date - 1 == array_of_dates[idx - 1] ? '-' : ', '
      range_string += "#{delimiter}#{date}"
      end_date = date.to_s
    # all dates in between
    else
      # date +1 equals next date in array and date -1 equals last date in array. ([1910,1911,1912] we are looking at 1912)
      next if date + 1 == array_of_dates[idx + 1] && date - 1 == array_of_dates[idx - 1]
      
      # date +1 equals next date in array and date -1 does not equal last date in array. ([1905,1911,1912] we are looking at 1911)
      if date + 1 == array_of_dates[idx + 1] && date - 1 != array_of_dates[idx - 1]
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

# Made with love by Andre for Hayley
