# ruby_python_csv_converter

## Scripts to manipulate CSV data. Written in Ruby and Python.

### Input/Output Directories
  * Copy your input CSV file into the `input_csv_files/` directory, make sure it has a `.csv` file name extension
  * Output CSV file will saved in `output_csv_files/` directory with the same name as the input file.

### To run Python script
In the command line, change directory to `python/` and enter:
```shellscript
python convert.py input_csv_file_name.csv your_command
```

### To run Ruby script
In the command line, change directory to `ruby/` and enter: 
```shellscript
ruby convert.rb input_csv_file_name.csv your_command
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
1. Create a new blank file with the respective extension in the respective directory
  * Ruby: `new_file_name.rb` in the `ruby/` directory  
  * Python: `new_file_name.py` in the `python/` directory  
2. Write functions for the new command in the above file
3. Import the new file into the `convert` file
  * Ruby: At the top of the `convert.rb` file, add
    ```Ruby 
    require_relative('new_file_name')
    ```
  * Python: At the top of the `convert.py` file, add
    ```Python
    from new_file_name import your_function_name_1 your_function_name_2
    ```
4. Inside the `convert` file, nest command-specific logic in an 'if' condition block.
  * Ruby
    ```Ruby 
    if command_option == "your_command"
       invoke_your_function()
    end
    ```
  * Python
    ```Python 
    if command_option == "your_command":
       invoke_your_function()
    ```
5. Profit. 

### Benchmarking
Using sample CSV file `time.csv` on MacBook Pro Mid 2015, 2.2 GHz Quad-Core Intel Core i7, 16 GB memory: 
  * Ruby
    ```shellscript 
    Script took 17.39 seconds to run
    ```
  * Python
    ```shellscript 
    Script took 5.38 seconds to run
    ```

