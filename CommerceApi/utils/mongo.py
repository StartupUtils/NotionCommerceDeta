from motor.motor_asyncio import AsyncIOMotorClient
from .CommerceApi.config import Config
from fastapi.encoders import jsonable_encoder


class Mongoify:
    CLIENT = AsyncIOMotorClient(Config.mongo_uri)
    DB = CLIENT.db

    @classmethod
    async def insert(cls, table, data):
        data = jsonable_encoder(data)
        result = await cls.DB[table].insert_one(data)
        return result

    @classmethod
    async def find_one(cls, table, query):
        return await cls.DB[table].find_one(query)

    @classmethod
    async def update(cls, table, query, update, upsert=True):
        return await cls.DB[table].update_one(query, {"$set": update}, upsert=upsert)
