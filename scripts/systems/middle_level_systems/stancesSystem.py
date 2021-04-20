from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.databaseManager import DatabaseManager as dM


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
