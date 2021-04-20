from scripts.database.databaseManager import DatabaseManager as dM
from typing import Union, List, Any


class UtilityFunctions:
    _class_template = None
    _collection = None

    @staticmethod
    def class_to_id(class_instance_or_int: Union[object, int]) -> int:
        if isinstance(class_instance_or_int, int):
            return class_instance_or_int
        return class_instance_or_int.id

    @classmethod
    def _insert_class_instance(cls, _id: int) -> bool:
        """Returns True if inserted successfully, False otherwise"""
        return dM.insert_one(cls._collection, cls._class_template(_id).json())

    @classmethod
    def _actualize_database_instance_to_class_template(cls, data: dict) -> bool:
        template = cls._class_template(0).json()
        for key in template.keys():
            if key not in data:
                return dM.update_one(cls._collection, {'_id': data['_id']}, {key: template[key]})

    @classmethod
    def _get_class_instance_from_database(cls, _id: int) -> Union[object, bool]:
        """Returns class instance from database, and actualizes schema, or returns False if something went wrong"""
        return cls._get_class_instance_from_database_by_query({'_id': _id})

    @classmethod
    def _get_class_instance_from_database_by_query(cls, query: dict) -> Union[object, bool]:
        """Returns class instance from database, and actualizes schema, or returns False if something went wrong"""
        data = dM.get_one(cls._collection, query)
        if data is not False:
            class_instance = cls._class_template(data["_id"]).load(data)
            if isinstance(class_instance, cls._class_template):
                return class_instance
            else:
                cls._actualize_database_instance_to_class_template(data)
                class_instance = cls._class_template(data["_id"]).load(data)
                if isinstance(class_instance, cls._class_template):
                    return class_instance
                else:
                    print("[Error]!!! in UtilityDatabase functions get one by query")
        return False

    @classmethod
    def _get_many_class_instances(cls, _ids_list: List[int], get_all=False) -> List[object]:
        """Returns list of class instances from database, and actualizes schemas"""
        if get_all:
            return cls._get_many_class_instances_by_query({})
        else:
            return cls._get_many_class_instances_by_query({'_id': {'$in': _ids_list}})

    @classmethod
    def _get_many_class_instances_by_query(cls, query: dict) -> List[object]:
        """Returns list of class instances from database, and actualizes schemas"""
        data_list = dM.get_many(cls._collection, query)
        class_instance_list = []
        for data in data_list:
            class_instance = cls._class_template(data['_id']).load(data)
            if isinstance(class_instance, cls._class_template):
                class_instance_list.append(class_instance)
            else:
                cls._actualize_database_instance_to_class_template(data)
                if isinstance(class_instance, cls._class_template):
                    class_instance_list.append(cls._class_template(data['_id']).load(data))
                else:
                    print("[Error]!!! in UtilityDatabase functions get many")
        return class_instance_list

    # PUBLIC METHODS

    @classmethod
    def create(cls, _id: int) -> bool:
        return cls._insert_class_instance(_id)

    @classmethod
    def get_one(cls, _id: int) -> Union[object, bool]:
        return cls._get_class_instance_from_database(_id)

    @classmethod
    def get_many(cls, _ids_list: List[int]) -> List[object]:
        return cls._get_many_class_instances(_ids_list)

    @classmethod
    def get_all(cls) -> List[object]:
        return cls._get_many_class_instances([], get_all=True)

    @classmethod
    def get_one_by_query(cls, query: dict) -> Union[object, bool]:
        return cls._get_class_instance_from_database_by_query(query)

    @classmethod
    def get_many_by_query(cls, query: dict) -> List[object]:
        return cls._get_many_class_instances_by_query(query)

    @classmethod
    def update_one(cls, _id: int, data_to_update: dict) -> bool:
        return dM.update_one(cls._collection, {'_id': _id}, data_to_update)
