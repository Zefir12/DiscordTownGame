from scripts.systems.utilities.utilityDatatbaseFunctions import UtilityFunctions as uF
from onlineMongoDB import TownDatabase as tD
from scripts.data_types.baseDatabaseClass import BaseDatabaseClass


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



