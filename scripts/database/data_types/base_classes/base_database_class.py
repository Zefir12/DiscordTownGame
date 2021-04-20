from typing import List
from scripts.database.errors.errors import *


class BaseDatabaseClass:
    _prevent_parameters_from_inserting: List[str] = []
    _prevent_parameters_from_loading: List[str] = []
    _change_value_name_during_inserting: Dict[str, str] = {'id': '_id'}
    _change_value_name_during_loading: Dict[str, str] = {'_id': 'id'}

    def __str__(self):
        return f'{type(self).__name__} object data: {str(self.__dict__)}'

    def json(self):
        json = {}
        for key in self.__dict__:
            if key not in self._prevent_parameters_from_inserting:
                new_key = key
                if new_key in self._change_value_name_during_inserting:
                    new_key = self._change_value_name_during_inserting[key]
                json[new_key] = self.__dict__[key]
        return json

    def load(self, data: Dict[str, Any]):
        for key in data:
            if key not in self._prevent_parameters_from_loading:
                new_key = key
                if key in self._change_value_name_during_loading:
                    new_key = self._change_value_name_during_loading[key]
                if new_key not in self.__dict__ and new_key not in self._prevent_parameters_from_loading:
                    raise UnknownKeyInDatabase(data, self, message='Unknown key in database')
                self.__dict__[new_key] = data[key]
        for key in self.__dict__:
            old_key = key
            if key in self._change_value_name_during_inserting:
                old_key = self._change_value_name_during_inserting[key]
            if old_key not in data and old_key not in self._prevent_parameters_from_inserting:
                raise KeyIsMissingInDatabase(data, self, message='Key is missing in database')
        return self


