from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass
from scripts.database.onlineMongoDB import TownDatabase as tD
from scripts.database.data_types.base_classes.base_database_system import UtilityFunctions as uF
from scripts.systems.middle_level_systems.itemSystem import ItemsSystem


class Inventory(BaseDatabaseClass):
    def __init__(self, _id):
        self._id = _id
        self.id = _id
        self.default_size = 40
        self.owner_id = _id
        self.backpack_size = 0
        self.storage_size = 1200


class InventorySystem(uF):
    _class_template = Inventory
    _collection = tD.eq

    @classmethod
    def get_free_inventory_space(cls, user_id: int) -> int:
        inventory = cls.get_one_by_query({'owner_id': user_id})
        if inventory is not False:
            items_count = ItemsSystem.check_how_many_items_user_has_on_him(user_id)
            space = inventory.default_size + inventory.backpack_size
            return space - items_count
        print('Couldnt get user inventory, [inventorySystem]')
        return False

    @classmethod
    def add_new_item(cls, item_template_id: int, inventory_id: int):
        ItemsSystem.create_from_template(item_template_id, inventory_id)

    @classmethod
    def change_owner(cls, _id: int, owner_id: int):
        return cls.update_one(_id, {'owner_id': owner_id})
