from scripts.systems.low_level_systems.databaseManager import DatabaseManager as dM
from scripts.data_types.baseDatabaseClass import BaseDatabaseClass
from onlineMongoDB import TownDatabase as tD
from scripts.systems.utilities.utilityDatatbaseFunctions import UtilityFunctions as uF


item_types = {
    0: 'normal',
    1: 'edible',
    2: 'clothes',
    3: 'weapon',
}

storage_type = {
    0: 'personal',
    1: 'storage'
}


class Item(BaseDatabaseClass):
    def __init__(self, _id):
        self._id = _id
        self.id = _id
        self.owner_id = _id
        self.type = 0
        self.type_reference = -1
        self.name = 'None'
        self.amount = 1
        self.storage = 0


class ItemsSystem(uF):
    _class_template = Item
    _collection = tD.items

    @classmethod
    def check_if_id_exists(cls, _id: int):
        if cls.get_one(_id) is not False:
            return True
        return False

    @classmethod
    def get_free_id(cls):
        new_id = cls.get_all().__len__() + 1
        if not cls.check_if_id_exists(new_id):
            return new_id
        for b in range(5):
            print('trying to get free id')
            new_id += 1
            if not cls.check_if_id_exists(new_id):
                return new_id

    @classmethod
    def check_how_many_items_user_has_on_him(cls, user_id: int):
        return cls.get_many_by_query({'owner_id': user_id, 'storage': 0}).__len__()

    @classmethod
    def create_from_template(cls, template_id: int, inventory_id: int):
        new_item_id = cls.get_free_id()
        cls.create(new_item_id)
        template_item = ItemsTemplateSystem.get_one(template_id)
        cls.update_one(new_item_id, {'type': template_item.type, 'type_reference': template_item.type_reference,
                                     'name': template_item.name, 'owner_id': inventory_id})

    @classmethod
    def get_item_name_from_id(cls):
        pass


class ItemTemplate(BaseDatabaseClass):
    def __init__(self, _id: int):
        self._id = _id
        self.id = _id
        self.type = 0
        self.type_reference = -1
        self.name = 'None'


class ItemsTemplateSystem(uF):
    _class_template = ItemTemplate
    _collection = tD.item_templates


class ItemPool(BaseDatabaseClass):
    def __init__(self, _id: int):
        self._id = _id
        self.id = _id
        self.name = "None"
        self.items = {}


class ItemsPoolSystem(uF):
    _class_template = ItemPool
    _collection = tD.item_pools

