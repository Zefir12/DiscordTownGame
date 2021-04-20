from scripts.database.databaseManager import DatabaseManager as dM
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF


class Stats(BaseDatabaseClass):
    def __init__(self, _id):
        self._id = _id
        self.id = _id
        self.owner_id = _id
        self.level = 1
        self.max_life = 100
        self.life_points = 100
        self.character_class = None
        self.experience = 0
        self.stance = 0
        self.status = 1
        self.place = 1


class StatsSystem(uF):
    _class_template = Stats
    _collection = tD.stats

    @classmethod
    def update_one_stat(cls, id_or_stats, stat_name, value_to_set):
        """Returns True if successful, False otherwise"""
        id_or_stats = uF.class_to_id(id_or_stats)
        return dM.update_one(tD.stats, {'_id': id_or_stats}, {stat_name: value_to_set})

    @classmethod
    def update_stats(cls, id_or_stats, data_to_update: dict):
        """Returns True if successful, False otherwise"""
        id_or_stats = uF.class_to_id(id_or_stats)
        return dM.update_one(tD.stats, {'_id': id_or_stats}, data_to_update)

    @staticmethod
    def increment_one_stat(_id: int, query: dict, stat_name: str, amount: float):
        return dM.increment_one(tD.stats, query, {stat_name: amount})

    @classmethod
    def change_stats_owner(cls, _id: int, owner_id: int):
        return cls.update_stats(_id, {'owner_id': owner_id})
