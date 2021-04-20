from scripts.database.databaseManager import DatabaseManager as dM
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass


class TownUser(BaseDatabaseClass):
    def __init__(self, _id):
        self.discord_nick = ''
        self.name = ''
        self._id = _id
        self.id = _id
        self.eq_id = -1
        self.wallet_id = -1
        self.stats_id = -1
        self.travel_destination = 0
        self.travel_time_left = 0


class PeopleSystem(uF):
    _class_template = TownUser
    _collection = tD.users

    @staticmethod
    def check_if_user_exist(_id):
        """Returns True if user is in database, False otherwise"""
        if not dM.get_one(tD.users, {'_id': _id}):
            return False
        return True

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
