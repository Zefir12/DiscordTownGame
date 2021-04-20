from typing import Dict, Any


class KeyIsMissingInDatabase(Exception):
    """Exception raised for errors in the loading of classes"""

    def __init__(self, data: Dict[str, Any], class_object: object, message='Default Message'):
        self.data = data
        self.object = class_object
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.object.__str__()}, {self.data} -> {self.message}"


class UnknownKeyInDatabase(Exception):
    """Exception raised for errors in the loading of classes"""

    def __init__(self, data: Dict[str, Any], class_object: object, message='Default Message'):
        self.data = data
        self.object = class_object
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.object.__str__()}, {self.data} -> {self.message}"