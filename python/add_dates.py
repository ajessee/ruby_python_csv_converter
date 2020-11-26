## create date object to hold date info for geographic region
# object will store key/value pair of CSV region name and dates array. Example:
# {
#   AACHEN: [1820, 1836, 1837, 1838....]
# }
def create_date_object(headers, new_column_headers_array, csv_objects_array):
  if 'Date' in headers:
    date_object = {}
    # populate date object 
    for csv_object in csv_objects_array:
      # dynamically add new column header attributes and attribute values to CSV object
      for new_column_header in new_column_headers_array:
        setattr(csv_object, new_column_header.replace(" ", "_").lower(), None)
      # if CSV object region name ('Name' column header) is already key in array, append date into value array
      if csv_object.name in date_object:
        date_object[csv_object.name].append(int(csv_object.date))
      # else, create key and array with first date value
      else:
        date_object[csv_object.name] = [int(csv_object.date)]
  return date_object

## add new column headers to existing header row from CSV file
def add_column_headers(headers, new_column_headers_array):
  for column_header in new_column_headers_array:
    headers.append(column_header)

## set new attributes in CSV object. In this case, we are adding "Start Date", "End Date", "Date Ranges"
def set_date_attributes_in_csv_obj(csv_object, date_object, headers):
  if 'Date' in headers and hasattr(csv_object, 'name'):
    # converting list to set will return only unique values
    unique_dates_set = set(date_object[csv_object.name])
    # sorting a set will return a list
    unique_dates_list = sorted(unique_dates_set)
    # set start date, end date, date ranges attributes in CSV object from return value of create_date_strings()
    csv_object.start_date, csv_object.end_date, csv_object.date_ranges = create_date_strings(unique_dates_list)

## test if row data for column is blank
def test_for_blank_row_data(headers, row, header_name, index):
  if headers[index] == header_name and row[index] == '':
    return True
  else:
    return False

## create string of date ranges
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
  # return array with start date, end date, range string
  return [start_date, end_date, range_string]

  # Made with love by Andre for Hayley
