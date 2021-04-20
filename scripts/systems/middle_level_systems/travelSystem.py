from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS
from scripts.database.databaseManager import DatabaseManager as dM
from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.database.onlineMongoDB import TownDatabase as tD


class Place(BaseDatabaseClass):
    def __init__(self, _id):
        self.name = "None"
        self.id = _id
        self._id = _id
        self.type = 0
        self.description = "None"
        self.url_image = "None"


class TravelSystem(uF):
    _class_template = Place
    _collection = tD.places

    @staticmethod
    def get_connection_between_places(id1: int, id2: int):
        """Returns one travel connection data from database"""
        query = {'id1': {'$in': [id1, id2]}, 'id2': {'$in': [id1, id2]}}
        return dM.get_one(tD.travel_connections, query)

    @staticmethod
    def check_if_user_travelling(_id: int):
        """Returns True if user have more than 0 [travel time left], False otherwise"""
        if pS.get_one(_id).travel_time_left > 0:
            return True
        return False

    @classmethod
    def set_user_travelling(cls, _id, destination: Place, time: float):
        return pS.update_user(_id, {'travel_destination': destination.id, 'travel_time_left': time * 60})

    @classmethod
    def set_user_finished_travelling(cls, _id):
        return pS.update_user(_id, {'travel_destination': 0, 'travel_time_left': 0})

    @staticmethod
    def inc_user_travel_time(_id, amount):
        return pS.increment_user(_id, {'travel_time_left': amount})

    @staticmethod
    def get_possible_travel_connections_to_travel(location_id):
        """Return list of travel connections"""
        list_of_travel_connections = []
        for travel_connection in dM.get_many(tD.travel_connections, {'$or': [{'id1': location_id}, {'id2': location_id}]}):
            list_of_travel_connections.append(travel_connection)
        return list_of_travel_connections

