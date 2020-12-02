# ruby_python_csv_converter

## Scripts to manipulate CSV data. Written in Ruby and Python.

### Input/Output Directories
  * Copy your input CSV file into the `input_csv_files/` directory, make sure it has a `.csv` file name extension
  * Output CSV file will saved in `output_csv_files/` directory with the same name as the input file.

### To run Ruby script
In the command line, change directory to `ruby/` and enter: 
```sh
ruby convert.rb input_csv_file_name.csv your_command
```

### To run Python script
In the command line, change directory to `python/` and enter:
```sh
python convert.py input_csv_file_name.csv your_command
```

### Troubleshooting
Make sure that you've done the following
  * make sure your CSV file is in the `input_csv_files/` directory
  * replace `input_csv_file_name.csv` with your CSV file name in full command
  * replace `your_command` with the command you want to run in full command

### Dependencies
* Ruby - You will need to install the `humanize` and `pry-byebug` gems. Run the following commands from the command line:
  ```Ruby
  gem install humanize && gem install pry-byebug
  ```
* Python - None

### Currently supported commands
`add_dates`
> If CSV file has a `Date` column, it will collect all dates (years in `2000` format) from each row that shares the same name from the `NAME` column, and then add a `Start Date` column that contains the earliest year found in `NAME` array of rows, an `End Date` column that contains the latest year found in `NAME` array of rows, and add a `Date Range` column that shows any gaps in years.

### Extending these scripts
To extend either script, use the following steps:
1. Create a new blank file with your class name (match to new command name) in the respective directory
  * Ruby: `new_class_name.rb` in the `ruby/` directory  
  * Python: `new_class_name.py` in the `python/` directory  
2. Build class in this file with the following static method(s)
  * Ruby: 
    ```Ruby 
    def self.===(args_array)
      args_array[0] == 'your_command_name'
    end

    def self.matcher(args_array)
      # look at the AddDates class for an example of how to build Case statement for your code
    end
    ```
  * Python:
    ```Python 
    def matcher(cls, args_array):
      # look at the AddDates class for an example of how to build conditional logic for your code
    ```
4. Add any other static methods to the class that you need for your command. Look at the `AddDates` class for guidance.
5. Import the new file (class) into the `convert` file
  * Ruby: At the top of the `convert.rb` file, add
    ```Ruby 
    require_relative('your_class')
    ```
  * Python: At the top of the `convert.py` file, add
    ```Python
    from new_file_name import YourClass
    ```
6. In your new file (class), put your code in the `matcher()` static method. Look at the `AddDates` class for guidance.
7. In `convert` file, add your command to the `command_logic()` function, and follow the pattern for your respective language.
  * Ruby:
    ```Ruby 
    def command_logic(command, stage, args)
      args_array = [command, stage, args]
      case args_array
      when AddDates
        return_object = AddDates.matcher(args_array)
      # to add new commands, add below
      # when YourClass
      #   return_object = YourClass.matcher(args_array)
      end
      return_object
    end
    ```
  * Python:
    ```Python
    def command_logic(command, stage, args):
        args_array = [command, stage, args]
        if command == 'add_dates':
            return_object = AddDates.matcher(AddDates, args_array)
        # to add new commands, add below
        # elif command == 'add_new_command_here':
        #     return_object = YourClass.matcher(YourClass, args_array)
        return return_object
    ```
8. Profit. 

### Benchmarking
All benchmarks use sample CSV file `time.csv`.

MacBook Pro Mid 2015, 2.2 GHz Quad-Core Intel Core i7, 16 GB memory: 
  * Ruby
    ```sh 
    Script took 17.39 seconds to run
    ```
  * Python
    ```sh 
    Script took 5.38 seconds to run
    ```
Raspberry Pi 4, 1.5 GHz Broadcom BCM2711, Quad core Cortex-A72 (ARM v8) 64-bit SoC, 8 GB memory: 
  * Ruby
    ```sh 
    Script took 75.56 seconds to run
    ```
  * Python
    ```sh 
    Script took 18.64 seconds to run
    ```
Yeah, apparently Python is 3x-4x faster than Ruby for this use case.

