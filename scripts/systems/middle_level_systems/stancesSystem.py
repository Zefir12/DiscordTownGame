from scripts.systems.utilities.utilityDatatbaseFunctions import UtilityFunctions as uF
from onlineMongoDB import TownDatabase as tD
from scripts.data_types.baseDatabaseClass import BaseDatabaseClass
from scripts.systems.low_level_systems.databaseManager import DatabaseManager as dM


class Stances(BaseDatabaseClass):
    def __init__(self, _id):
        self.name = "None"
        self.id = _id
        self._id = _id
        self.description = "None"
        self.url_image = "None"


class StancesSystem(uF):
    _class_template = Stances
    _collection = tD.stances_dict

    @classmethod
    def update_one_stat(cls, id_or_stance, stat_name, value_to_set):
        """Returns True if successful, False otherwise"""
        id_or_stance = cls.class_to_id(id_or_stance)
        return dM.update_one(cls._collection, {'_id': id_or_stance}, {stat_name: value_to_set})
