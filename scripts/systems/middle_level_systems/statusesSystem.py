from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass


class Status(BaseDatabaseClass):
    def __init__(self, _id):
        self.name = "None"
        self.id = _id
        self._id = _id
        self.description = "None"
        self.url_image = "None"


class StatusesSystem(uF):
    _class_template = Status
    _collection = tD.statuses_dict



