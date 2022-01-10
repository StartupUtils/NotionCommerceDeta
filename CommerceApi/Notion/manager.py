import requests, json
from CommerceApi.models.notion import NotionObject
from CommerceApi.config import Config


class NotionClient:
    url = "https://api.notion.com/v1"
    session = requests.Session()
    session.headers = {
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16",
        "Authorization": f"Bearer {Config.notion_token}",
    }

    @classmethod
    def get_info(cls, page_id, target="databases"):
        return cls.session.request("GET", f"{cls.url}/{target}/{page_id}")

    @classmethod
    def get_block_children(cls, page_id):
        return cls.session.request("GET", f"{cls.url}/blocks/{page_id}/children")

    @classmethod
    def update(cls, database_id, data, target="databases"):
        print(f"{cls.url}/databases/{database_id}")
        return cls.session.request(
            "PATCH", f"{cls.url}/{target}/{database_id}", json=data
        )

    @classmethod
    def update_block(cls, page_id, data):
        return cls.session.request("PATCH", f"{cls.url}/blocks/{page_id}", json=data)

    @classmethod
    def append_block_children(cls, page_id, data):
        return cls.session.request(
            "PATCH", f"{cls.url}/blocks/{page_id}/children", json=data
        )

    @classmethod
    def create_database(cls, data):
        return cls._create(data, target="databases")

    @classmethod
    def create_page(cls, data):
        return cls._create(data, target="pages")

    @classmethod
    def _create(cls, data, target="databases"):
        return cls.create_object(
            cls.session.request("POST", f"{cls.url}/{target}", json=data)
        )

    @classmethod
    def query_database(cls, database_id, data={}):
        return cls.session.request(
            "POST", f"{cls.url}/databases/{database_id}/query", json=data
        )

    @staticmethod
    def create_object(response):
        if response.ok:
            return NotionObject(**response.json())
        else:
            print(response.json())
            return NotionObject(**response.json())
