class CsvObject:

  # instance method to return values of all object properties above
  def to_csv(self):
    return [*self.__dict__.values()]
