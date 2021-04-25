from pymongo.collection import Collection
from pymongo.results import UpdateResult
from typing import Any, Dict, List
from scripts.database.errors.errors import CannotFindItemInDatabase


class DatabaseManager:

    @staticmethod
    def delete_one(collection: Collection, query):
        """Returns True if successfully deleted, False otherwise"""
        return collection.delete_one(query).deleted_count == 1

    @staticmethod
    def delete_many(collection: Collection, query):
        """Returns number of deleted items"""
        return collection.delete_many(query).deleted_count

    @staticmethod
    def delete_all(collection: Collection):
        """Returns number of deleted items"""
        return collection.delete_many({}).deleted_count

    @staticmethod
    def update_one(collection: Collection, query, data_to_update):
        """Returns True if successfully updated, False otherwise"""
        return collection.update_one(query, {'$set': data_to_update}).matched_count == 1

    @staticmethod
    def update_many(collection: Collection, query, data_to_update):
        """Returns number of modified items"""
        return collection.update_many(query, {'$set': data_to_update}).matched_count

    @staticmethod
    def update_all(collection: Collection, data_to_update):
        """Returns number of modified items"""
        return collection.update_many({}, {'$set': data_to_update}).matched_count

    @staticmethod
    def get_one(collection: Collection, query: Dict[str, Any]):
        """Returns single item, false if found nothing"""
        data = collection.find_one(query)
        if data is None:
            raise CannotFindItemInDatabase(query, data)
        return data

    @staticmethod
    def get_many(collection, query: dict, selection=None) -> List[dict]:
        """Returns items in array"""
        data = []
        if selection is None:
            for item in collection.find(query):
                data.append(item)
        else:
            for item in collection.find(query, selection):
                data.append(item)
        return data

    @staticmethod
    def get_all(collection):
        """Returns items in array"""
        data = []
        for item in collection.find({}):
            data.append(item)
        return data

    @staticmethod
    def insert_one(collection, data):
        """Returns True if inserted successfully"""
        try:
            return collection.insert_one(data).inserted_id == data['_id']
        except Exception as error:
            print(error)
            raise

    @staticmethod
    def insert_many(collection, data):
        """Returns inserted _id's, false if something went wrong """
        try:
            return collection.insert_many(data).inserted_ids
        except Exception as error:
            print(error)
            raise

    @staticmethod
    def increment_one(collection: Collection, query, data):
        """Returns True if successfully incremented, false otherwise"""
        return collection.update_one(query, {'$inc': data}).modified_count == 1

    @staticmethod
    def increment_many(collection: Collection, query, data):
        """Returns number of incremented items"""
        return collection.update_many(query, {'$inc': data}).modified_count

    @staticmethod
    def increment_all(collection: Collection, data):
        """Returns number of incremented items"""
        return collection.update_many({}, {'$inc': data}).modified_count

    @staticmethod
    def remove_field(collection: Collection, query: Dict[str, Any], field: str):
        return collection.update_one(query, {'$unset': {field: 1}}).matched_count == 1

    @staticmethod
    def remove_fields(collection: Collection, query: Dict[str, Any], fields: List[str]) -> int:
        fields_to_remove = {}
        for field in fields:
            fields_to_remove[field] = 1
        return collection.update_one(query, {'$unset': fields_to_remove}).matched_count





