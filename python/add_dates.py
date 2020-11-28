# class for add_dates command
class AddDates:
    # setup class variable to hold date object
    date_object = None
    # create date object to hold date info for geographic region
    # object will store key/value pair of CSV region name and dates array. Example:
    # {
    #   AACHEN: [1820, 1836, 1837, 1838....]
    # }
    @staticmethod
    def create_date_object(headers, new_column_headers_array, csv_objects_array):
        if 'Date' in headers:
            date_object = {}
            # populate date object
            for csv_object in csv_objects_array:
                # dynamically add new column header attributes and attribute values to CSV object
                for new_column_header in new_column_headers_array:
                    setattr(csv_object, new_column_header.replace(
                        " ", "_").lower(), None)
                # if CSV object region name ('Name' column header) is already key in array, append date into value array
                if csv_object.name in date_object:
                    date_object[csv_object.name].append(int(csv_object.date))
                # else, create key and array with first date value
                else:
                    date_object[csv_object.name] = [int(csv_object.date)]
            return date_object

    # add new column headers to existing header row from CSV file
    @staticmethod
    def add_column_headers(cls, headers, new_column_headers_array):
        for column_header in new_column_headers_array:
            headers.append(column_header)

    # set new attributes in CSV object. In this case, we are adding "Start Date", "End Date", "Date Ranges"
    @staticmethod
    def set_date_attributes_in_csv_obj(cls, csv_object, date_object, headers):
        if 'Date' in headers and hasattr(csv_object, 'name'):
            # converting list to set will return only unique values
            unique_dates_set = set(date_object[csv_object.name])
            # sorting a set will return a list
            unique_dates_list = sorted(unique_dates_set)
            # set start date, end date, date ranges attributes in CSV object from return value of create_date_strings()
            csv_object.start_date, csv_object.end_date, csv_object.date_ranges = cls.create_date_strings(
                unique_dates_list)

    # test if row data for column is blank
    @staticmethod
    def test_for_blank_row_data(headers, row, header_name, index):
        if headers[index] == header_name and row[index] == '':
            return True
        else:
            return False

    # create string of date ranges
    @staticmethod
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

    # utility static method to run different logic based on stage of operations from convert.rb script
    @staticmethod
    def matcher(cls, args_array):
        return_object = None
        match_array = args_array[0:2]
        command_args = args_array[2]
        if match_array == ['add_dates', 'read']:
            # if name column is blank, skip creating a csv object
            return_object = cls.test_for_blank_row_data(
                command_args["headers"], command_args["row"], 'NAME', 5)
        elif match_array == ['add_dates', 'setup']:
            # column headers to add to CSV file
            new_column_headers_array = [
                "Start Date", "End Date", "Date Ranges"]
            # add new headers to existing headers
            cls.add_column_headers(cls,
                command_args["headers"], new_column_headers_array)
            # create date object and store in class variable
            cls.date_object = cls.create_date_object(
                command_args["headers"], new_column_headers_array, command_args["csv_objects_array"])
        elif match_array == ['add_dates', 'write']:
            cls.set_date_attributes_in_csv_obj(cls,
                command_args["csv_object"], cls.date_object, command_args["headers"])
        return return_object

# Made with love by Andre for Hayley
