import json
import os
import uuid
from decouple import config


class Config:
    base_page_id = str(uuid.UUID(config("notion_page_id")))
    notion_token = config("notion_token")
    base_url = config("base_url")
    deta_key = config("deta_key", None)
    stripe_key = config("stripe_key")
