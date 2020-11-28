# frozen_string_literal: true

# CsvObject class
class CsvObject
  # no initialize method needed - we are dynamically adding all object properties after object has been instantiatede

  # instance method to return values of all object properties
  def to_csv
    csv_array = []
    instance_variables.each do |attribute|
      csv_array.push(instance_variable_get(attribute))
    end
    csv_array
  end
end