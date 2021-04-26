from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.systems.low_level_systems.peopleSystem import PeopleSystem as pS, TownUser
from scripts.systems.middle_level_systems.travelSystem import TravelSystem as tS
from scripts.systems.middle_level_systems.itemSystem import ItemsSystem as iS
from scripts.systems.low_level_systems.statsSystem import StatsSystem as sS
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.systems.middle_level_systems.itemSystem import ItemsPoolSystem
from scripts.systems.middle_level_systems.inventorySystem import InventorySystem
from typing import List
import random


class Event(BaseDatabaseClass):
    def __init__(self, _id):
        self.name = "None"
        self.type = 1
        self.id = _id
        self.standard_chance_to_accept = 0.1
        self.chance_to_occur = 0.1
        self.item_pool = {}
        self.enemy_pool = {}
        self.places = {}
        self.types_of_places = {}
        self.status_modifiers = {}
        self._id = _id
        self.description = "None"


class EventResults:
    def __init__(self, user_id):
        self.user_id = user_id
        self.event_name = ''
        self.received_items_ids: List[int] = []

    def get_received_item_as_string(self) -> str:
        items_not_duplicated = {}
        for id in self.received_items_ids:
            if id not in items_not_duplicated:
                items_not_duplicated[id] = 1
            else:
                items_not_duplicated[id] += 1
        string = f''
        for item in items_not_duplicated:
            string += f"{iS.get_item_name_from_template_id(item)} x{items_not_duplicated[item]}, "
        if items_not_duplicated.__len__() == 0:
            string = 'Nothing'
        return string


class EventSystem(uF):
    _class_template = Event
    _collection = tD.events

    @classmethod
    def select_by_chances(cls, dictionary: dict, guaranteed=False):
        """For dicts that have [value_name: 0.213] <- chance type"""
        """Care! Its always changes first value into string!"""
        selected = []
        for key in dictionary:
            if dictionary[key] >= random.random():
                selected.append(key)
        if selected.__len__() == 0:
            if guaranteed:
                for key in dictionary:
                    selected.append(key)
                    return selected
        return selected

    @classmethod
    def get_random_event(cls):
        all_events = cls.get_all()
        successful_events = []

        for event in all_events:
            if random.random() <= event.chance_to_occur:
                successful_events.append(event)

        if len(successful_events) > 0:
            return random.choice(successful_events)
        return False

    @classmethod
    def get_compatible_users(cls, event: Event) -> list:
        """Returns list of TownUser objects"""
        # get all places affected
        compatible_places = cls.select_by_chances(event.places)
        compatible_types_of_places = cls.select_by_chances(event.types_of_places)
        compatible_places += [place.id for place in tS.get_many_by_query({'type': {'$in': compatible_types_of_places}})]

        # get all stats of players that are in correct places
        stats_list = sS.get_many_by_query({'place': {'$in': [int(place_id) for place_id in compatible_places]}})
        compatible_users = []
        for stat in stats_list:
            standard_chance = event.standard_chance_to_accept
            if stat.stance in event.status_modifiers:
                standard_chance *= event.status_modifiers[stat]
            if standard_chance >= random.random():
                compatible_users.append(pS.get_one(stat.owner_id))
        return compatible_users

    @classmethod
    def get_item_pools_ids(cls, event: Event) -> list:
        """Always get at least first item pool in dict if nothing else was picked
        Returns list of item pools"""
        item_pool_list_ids = [int(item) for item in cls.select_by_chances(event.item_pool, guaranteed=True)]
        return item_pool_list_ids

    @classmethod
    def get_items_ids_from_item_pools(cls, list_of_pool_ids: list):
        item_ids_list = []
        for pool_id in list_of_pool_ids:
            item_ids_list += [int(item) for item in cls.select_by_chances(ItemsPoolSystem.get_one(pool_id).items)]

        if not item_ids_list:
            for pool_id in list_of_pool_ids:
                return [int(item) for item in cls.select_by_chances(ItemsPoolSystem.get_one(pool_id).items, guaranteed=True)]

        return item_ids_list

    @classmethod
    def give_items_to_inventory_from_item_pools_ids(cls, inventory_id: int, item_pool_ids: list):
        list_of_items_ids = cls.get_items_ids_from_item_pools(item_pool_ids)
        free_space = InventorySystem.get_free_inventory_space(inventory_id)

        # reduce list to how much space there is
        list_of_items_ids = list_of_items_ids[0:free_space]

        for item in list_of_items_ids:
            InventorySystem.add_new_item(item, inventory_id)
        return list_of_items_ids

    @classmethod
    def handle_event(cls, event: Event) -> list:
        """Returns list of [EventResult] objects"""
        users: List[TownUser] = cls.get_compatible_users(event)
        item_pool_ids = cls.get_item_pools_ids(event)
        list_of_event_results = []
        for user in users:
            event_result = EventResults(user.id)
            #print(user.name, user.id, user.eq_id)
            event_result.received_items_ids = cls.give_items_to_inventory_from_item_pools_ids(user.eq_id, item_pool_ids)
            event_result.event_name = event.name
            list_of_event_results.append(event_result)
        return list_of_event_results
