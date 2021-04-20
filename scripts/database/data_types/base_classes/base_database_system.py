from scripts.database.databaseManager import DatabaseManager as dM
from typing import Union, List, Any
from scripts.database.errors.errors import CannotFindItemInDatabase, KeysAreMissingInDatabase, UnknownKeyInDatabase


class UtilityFunctions:
    _class_template = None
    _collection = None

    @staticmethod
    def class_to_id(class_instance_or_int: Union[Any, int]) -> int:
        if isinstance(class_instance_or_int, int):
            return class_instance_or_int
        return class_instance_or_int.id

    @classmethod
    def _insert_class_instance(cls, _id: int) -> bool:
        """Returns True if inserted successfully, False otherwise"""
        return dM.insert_one(cls._collection, cls._class_template(_id).json())

    @classmethod
    def _actualize_database_instance_to_class_template(cls, id: int,  data: dict):
        template = cls._class_template(id).json()
        for key in template.keys():
            if key not in data:
                dM.update_one(cls._collection, {'_id': id}, {key: template[key]})

    @classmethod
    def _remove_fields_from_database_instance(cls, id: int, fields: List[str]):
        return dM.remove_fields(cls._collection, {'_id': id}, fields)

    @classmethod
    def _get_class_instance_from_database(cls, _id: int) -> Union[Any, bool]:
        """Returns class instance from database, and actualizes schema, or returns False if something went wrong"""
        try:
            return cls._get_class_instance_from_database_by_query({'_id': _id})
        except CannotFindItemInDatabase:
            raise

    @classmethod
    def _get_class_instance_from_database_by_query(cls, query: dict) -> Any:
        """Returns class instance from database, and actualizes schema, or returns False if something went wrong"""
        try:
            data = dM.get_one(cls._collection, query)
        except CannotFindItemInDatabase as err:
            print(err)
            raise
        else:
            try:
                class_instance = cls._class_template(data["_id"]).load(data)
            except KeysAreMissingInDatabase as err:
                cls._actualize_database_instance_to_class_template(data["_id"], data)
                print(err)
                return cls._class_template(data["_id"]).load(data)
            except UnknownKeyInDatabase as err:
                cls._remove_fields_from_database_instance(data["_id"], err.keys_list)
                print(err)
                return cls._class_template(data["_id"]).load(data)
            else:
                return class_instance

    @classmethod
    def _get_many_class_instances(cls, _ids_list: List[int], get_all=False) -> List[Any]:
        """Returns list of class instances from database, and actualizes schemas"""
        if get_all:
            return cls._get_many_class_instances_by_query({})
        else:
            return cls._get_many_class_instances_by_query({'_id': {'$in': _ids_list}})

    @classmethod
    def _get_many_class_instances_by_query(cls, query: dict) -> List[Any]:
        """Returns list of class instances from database, and actualizes schemas"""
        data_list = dM.get_many(cls._collection, query)
        class_instance_list = []
        for data in data_list:
            try:
                class_instance = cls._class_template(data["_id"]).load(data)
            except KeysAreMissingInDatabase as err:
                cls._actualize_database_instance_to_class_template(data["_id"], data)
                print(err)
                class_instance_list.append(cls._class_template(data["_id"]).load(data))
            except UnknownKeyInDatabase as err:
                cls._remove_fields_from_database_instance(data["_id"], err.keys_list)
                print(err)
                class_instance_list.append(cls._class_template(data["_id"]).load(data))
            else:
                class_instance_list.append(class_instance)
        return class_instance_list

    # PUBLIC METHODS

    @classmethod
    def create(cls, _id: int) -> bool:
        return cls._insert_class_instance(_id)

    @classmethod
    def get_one(cls, _id: int) -> Union[Any, bool]:
        try:
            return cls._get_class_instance_from_database(_id)
        except CannotFindItemInDatabase as err:
            print(err)
            raise

    @classmethod
    def get_many(cls, _ids_list: List[int]) -> List[Any]:
        return cls._get_many_class_instances(_ids_list)

    @classmethod
    def get_all(cls) -> List[Any]:
        return cls._get_many_class_instances([], get_all=True)

    @classmethod
    def get_one_by_query(cls, query: dict) -> Union[Any, bool]:
        try:
            return cls._get_class_instance_from_database_by_query(query)
        except CannotFindItemInDatabase as err:
            print(err)
            raise

    @classmethod
    def get_many_by_query(cls, query: dict) -> List[Any]:
        return cls._get_many_class_instances_by_query(query)

    @classmethod
    def update_one(cls, _id: int, data_to_update: dict) -> bool:
        return dM.update_one(cls._collection, {'_id': _id}, data_to_update)
