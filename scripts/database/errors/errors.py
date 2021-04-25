from typing import Dict, Any, List


class KeysAreMissingInDatabase(Exception):
    """Exception raised for errors in the loading of classes"""

    def __init__(self, data: Dict[str, Any], class_object: object, message='Key is missing in database'):
        self.data = data
        self.object = class_object
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.message}] -> {self.object.__str__()}, {self.data}"


class UnknownKeyInDatabase(Exception):
    """Exception raised for errors in the loading of classes"""

    def __init__(self, data: Dict[str, Any], class_object: object, keys_list: List[str],  message='Unknown key in database'):
        self.data = data
        self.keys_list = keys_list
        self.object = class_object
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.message}] -> [Keys]: {self.keys_list}, {self.object.__str__()}, {self.data}"


class CannotFindItemInDatabase(Exception):
    def __init__(self, data: Dict[str, Any], returned_object: Any, message='Cannot find item in the database'):
        self.item_id = data
        self.object = returned_object
        self.message = message
        print(f"[{self.message}] -> [Return]: {self.object.__str__()}, [Query]: {self.item_id}")
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.message}] -> [Return]: {self.object.__str__()}, [Query]: {self.item_id}"