from scripts.database.databaseManager import DatabaseManager as dM
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from pymongo.collection import Collection
from scripts.database.errors.errors import CannotFindItemInDatabase


class TownUser(BaseDatabaseClass):
    def __init__(self, _id):
        self.discord_nick: str = ''
        self.name: str = ''
        self.id: int = _id
        self.eq_id: int = -1
        self.wallet_id: int = -1
        self.stats_id: int = -1
        self.travel_destination: int = 0
        self.travel_time_left: int = 0


class PeopleSystem(uF):
    _class_template: TownUser = TownUser
    _collection: Collection = tD.users

    @classmethod
    def check_if_user_exist(cls, id) -> bool:
        """Returns True if user is in database, False otherwise"""
        try:
            cls.get_one(id)
            return True
        except CannotFindItemInDatabase:
            return False

    @staticmethod
    def update_user(_id, data):
        return dM.update_one(tD.users, {'_id': _id}, data)

    @staticmethod
    def update_many_users(_ids, data):
        """Returns number of updated users"""
        return dM.update_many(tD.users, {'_id': {'$in': _ids}}, data)

    @staticmethod
    def update_all_users(data):
        """Returns number of updated users"""
        return dM.update_all(tD.users, data)

    @staticmethod
    def increment_user(_id, data):
        """Returns true if successfully incremented, False otherwise"""
        return dM.increment_one(tD.users, {'_id': _id}, data)

    @staticmethod
    def increment_many_users(_ids, data):
        """Returns number of incremented users"""
        return dM.increment_many(tD.users, {'_id': {'$in': _ids}}, data)

    @staticmethod
    def increment_all_users(data):
        """Returns number of incremented users"""
        return dM.increment_all(tD.users, data)

    @staticmethod
    def delete_user(_id):
        """Returns true if successfully deleted, False otherwise"""
        return dM.delete_one(tD.users, {'_id': _id})
