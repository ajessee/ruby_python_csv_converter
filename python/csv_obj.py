class CsvObject:
    # no __init__ method needed - we are dynamically adding all object properties after object has been instantiated

    # instance method to return values of all object properties
    def to_csv(self):
        return [*self.__dict__.values()]
