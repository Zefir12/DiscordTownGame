
class DatabaseManager:

    @staticmethod
    def delete_one(collection, query):
        """Returns True if successfully deleted, False otherwise"""
        return collection.delete_one(query).deleted_count == 1

    @staticmethod
    def delete_many(collection, query):
        """Returns number of deleted items"""
        return collection.delete_many(query).deleted_count

    @staticmethod
    def delete_all(collection):
        """Returns number of deleted items"""
        return collection.delete_many({}).deleted_count

    @staticmethod
    def update_one(collection, query, data_to_update):
        """Returns True if successfully updated, False otherwise"""
        return collection.update_one(query, {'$set': data_to_update}).modified_count == 1

    @staticmethod
    def update_many(collection, query, data_to_update):
        """Returns number of modified items"""
        return collection.update_many(query, {'$set': data_to_update}).modified_count

    @staticmethod
    def update_all(collection, data_to_update):
        """Returns number of modified items"""
        return collection.update_many({}, {'$set': data_to_update}).modified_count

    @staticmethod
    def get_one(collection, query):
        """Returns single item, false if found nothing"""
        data = []
        for item in collection.find(query):
            data.append(item)
        if data.__len__() > 0:
            return data[0]
        return False

    @staticmethod
    def get_many(collection, query, selection=None):
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
        """Returns True if inserted successfully, False otherwise"""
        try:
            return collection.insert_one(data).inserted_id == data['_id']
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def insert_many(collection, data):
        """Returns inserted _id's, false if something went wrong """
        try:
            return collection.insert_many(data).inserted_ids
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def increment_one(collection, query, data):
        """Returns True if successfully incremented, false otherwise"""
        return collection.update_one(query, {'$inc': data}).modified_count == 1

    @staticmethod
    def increment_many(collection, query, data):
        """Returns number of incremented items"""
        return collection.update_many(query, {'$inc': data}).modified_count

    @staticmethod
    def increment_all(collection, data):
        """Returns number of incremented items"""
        return collection.update_many({}, {'$inc': data}).modified_count










