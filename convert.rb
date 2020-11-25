require_relative('geo_obj')
require 'csv'
require 'pry-byebug'

if ARGV.any?
  file_name = ARGV.first
  options = ARGV[1..-1]

  geo_objects_array = []
  incoming_csv_headers = CSV.open(file_name, &:readline)
  incoming_csv_headers.push("Start Date")
  incoming_csv_headers.push("End Date")
  incoming_csv_headers.push("Date Ranges")
  new_file_name = 'new_' + file_name

  # create array of geo objects
  CSV.foreach(file_name, headers: true) do |row|
    row_hash = row.to_h
    new_hash = {}
    row_hash.keys.each_with_index do |key, index|
      new_key = key.downcase.to_sym
      new_key = :f_id if index == 0
      new_key = :two_kreis_ke if key == "2_Kreis_Ke"
      new_hash[new_key] = row_hash[key] if row_hash[key]        
    end
    geo_objects_array << GeoObject.new(new_hash) if new_hash[:name]
  end

  # create object to store geo region name and date array
  # {
  #   AACHEN: [1820, 1836]
  # }

  date_object = {}

  geo_objects_array.each do |geo_object|
    if date_object[geo_object.name]
      date_object[geo_object.name].push(geo_object.date.to_i)
    else
      date_object[geo_object.name] = [geo_object.date.to_i]
    end
  end

  def create_date_strings(array_of_dates)
    start_date = ""
    end_date = ""
    range_string = ""
    array_of_dates.sort.each_with_index do |date, idx|
      if idx == 0
        range_string += date.to_s
        start_date = date.to_s
        end_date = date.to_s if array_of_dates.length == idx + 1
      elsif idx + 1 == array_of_dates.length
        delimiter = ""
        if date - 1 == array_of_dates[idx - 1]
          delimiter += "-"
        else
          delimiter += ", "
        end
        range_string += "#{delimiter}#{date}"
        end_date = date.to_s
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
    [start_date, end_date, range_string]
  end

  CSV.open(new_file_name, 'wb') do |csv|
    csv << incoming_csv_headers
    geo_objects_array.each do |geo_object|
      geo_object.start_date, geo_object.end_date, geo_object.date_ranges = create_date_strings(date_object[geo_object.name].uniq)
      csv << geo_object.to_csv
    end
  end

end



