from pymongo.mongo_client import MongoClient
import config


class ServiceConnector:
    def __init__(self, **services):
        if "mongodb" in services:
            try:
                self.mongo_client = MongoClient(
                    f'mongodb+srv://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_SERVER}/?retryWrites=true&w=majority')
            except Exception as e:
                raise e

            if "db" in services["mongodb"]:
                self.mongo_db = self.mongo_client[services["mongodb"]["db"]]



    def insert_row_mongo(self, collection, row):
        temp_collection = self.mongo_db[collection]
        result = temp_collection.find_one({"id": row["id"]})
        if result is not None:
            return None
        try:
            return temp_collection.insert_one(row)
        except Exception as e:
            raise e


