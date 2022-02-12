from deta import Deta
from CommerceApi.config import Config
from fastapi.encoders import jsonable_encoder


class DETA:
    if Config.deta_key:
        CLIENT = Deta(Config.deta_key)
    else:
        CLIENT = Deta(Config.deta_key)


class DetaBase(DETA):
    def __init__(self, table):
        self.DB = self.CLIENT.AsyncBase(table)

    async def insert(self, data):
        print(data)
        data = jsonable_encoder(data)
        result = await self.DB.put(data)
        return result

    async def get(self, key):
        return await self.DB.get(key)

    async def find_one(self, query):
        res = await self.DB.fetch(query)
        for data in res.items:
            return data

    async def find_many(self, query):
        res = await self.DB.fetch(query)
        return res.items

    async def update(self, query: dict, key: str):
        return await self.DB.update(query, key)

    async def put(self, query: dict):
        return await self.DB.put(query)
