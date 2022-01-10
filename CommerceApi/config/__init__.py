import json
import os
import uuid

# config_data = json.load(
#     open(os.path.dirname(os.path.realpath(__file__)) + "/data/config.json")
# )


class Config:
    mongo_uri = "mongodb://root:rootpassword@0.0.0.0:27017"
    base_page_id = str(uuid.UUID("2137d1dc534b4e66b92c17c8f8d277cd"))
    notion_token = 
    base_url = "http://0.0.0.0:3000"
    deta_key = 
