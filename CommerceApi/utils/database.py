from deta import Deta
from CommerceApi.config import Config
from fastapi.encoders import jsonable_encoder


class DetaBase:
    CLIENT = Deta(Config.deta_key)

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
        print(res)
        print(res.items)
        for data in res.items:
            return data

    async def find_many(self, query):
        res = await self.DB.fetch(query)
        return res.items

    async def update(self, query: dict, key: str):
        return await self.DB.update(query, key)