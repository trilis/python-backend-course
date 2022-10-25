from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db_client = client["results_db"]


class Db:
    def set(self, key: str, value: str):
        db_client["results"].insert_one({"key": key, "value": value})

    def get(self, key: str) -> str:
        return db_client["results"].find_one({"key": key})["value"]

    def has(self, key: str) -> bool:
        return db_client["results"].find_one({"key": key}) is not None
