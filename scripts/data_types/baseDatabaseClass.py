class BaseDatabaseClass:

    def __str__(self):
        return f'{type(self).__name__} object data: {str(self.__dict__)}'

    def json(self):
        return self.__dict__

    def load(self, data):
        for key in self.__dict__:
            if key not in data:
                return False
        self.__dict__ = data
        return self
