import csv
import sys
import pdb
from geo_obj import GeoObject

# will only run if you provide file name in command line: 'python convert.py [csv_file_name]'
if (len(sys.argv) > 1):

  file_name = sys.argv[1]
  # options aren't being used now, but you can extend this in the future if you want
  options = sys.argv[1:]
  # array of geo objects, which represent a row in the CSV file
  geo_objects_array = []
  new_file_name = 'new_' + file_name

  with open(file_name, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader, None)
    # there is a \ufeff character in the fid column name ('\ufefffid'), so we replace it with just 'fid'. You should probably reformat your spreadsheet column names
    headers[0] = 'fid'
    # Append the new column names to the end of existing header array
    headers.append("Start Date")
    headers.append("End Date")
    headers.append("Date Ranges")

    for row in reader:
      # if name column is blank (row[5]), skip creating a geo object (will delete this row from new CSV file)
      if row[5] == '':
        continue
      # create geo object and append to array
      geo_objects_array.append(GeoObject(*row))
  
  # blank object store key/value pair of geo region name and dates array. Example:
  # {
  #   AACHEN: [1820, 1836, 1837, 1838....]
  # }
  date_object = {}

  for geo_obj in geo_objects_array:
    # if geo region name is already key in array, append date into value array
    if geo_obj.name in date_object:
      date_object[geo_obj.name].append(int(geo_obj.date))
    # else, create key and array with first date value
    else:
      date_object[geo_obj.name] = [int(geo_obj.date)]

  # helper function to create string of date ranges
  def create_date_strings(array_of_dates):
    start_date = ""
    end_date = ""
    range_string = ""
    for idx, date in enumerate(array_of_dates):
      # first date in array
      if idx == 0:
        range_string += str(date)
        start_date = str(date)
        if len(array_of_dates) == idx + 1:
          end_date = str(date)
        continue
      # last date in array
      elif idx + 1 == len(array_of_dates):
        delimiter = ""
        if date - 1 == array_of_dates[idx - 1]:
          delimiter += "-"
        else:
          delimiter += ", "
        range_string += f'{delimiter}{date}'
        end_date = str(date)
        continue
      # all dates in between
      else:
        # date +1 equals next date in array and date -1 equals last date in array. ([1910,1911,1912] we are looking at 1912).
        if date + 1 == array_of_dates[idx + 1] and date - 1 == array_of_dates[idx - 1]:
          continue
        # date +1 equals next date in array and date -1 does not equal last date in array. ([1905,1911,1912] we are looking at 1911)
        elif date + 1 == array_of_dates[idx + 1] and date - 1 != array_of_dates[idx - 1]:
          range_string += f', {date}'
          continue
        # date +1 does not equal next date in array and date -1 does equal last date in array. ([1910,1911,1920] we are looking at 1911)
        elif date + 1 != array_of_dates[idx + 1] and date - 1 == array_of_dates[idx - 1]:
          range_string += f'-{date}'
          continue
        # date +1 does not equal next date in array and date -1 does not equal last date in array. ([1910,1915,1920] we are looking at 1915)
        elif date + 1 != array_of_dates[idx + 1] and date - 1 != array_of_dates[idx - 1]:
          range_string += f', {date}'
          continue
    # return array with start date, end date, range string.
    return [start_date, end_date, range_string]

  with open(new_file_name, 'w') as new_file:
    file_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write original row headers plus the start date, end date, date ranges headers we added
    file_writer.writerow(headers)

    for geo_obj in geo_objects_array:
      # get array of dates with only unique values
      unique_dates_set = set(date_object[geo_obj.name])
      unique_dates_list = list(unique_dates_set)
      
      # assign start date, end date, date ranges values to geo object
      geo_obj.start_date, geo_obj.end_date, geo_obj.date_ranges = create_date_strings(unique_dates_list)
      # write CSV row using GeoObject instance method that returns array of object properties
      file_writer.writerow(geo_obj.to_csv())
      
