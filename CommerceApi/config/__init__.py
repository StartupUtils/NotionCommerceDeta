import json
import os
import uuid
from decouple import config

class Config:
    base_page_id = str(uuid.UUID(config("notion_page_id")))
    notion_token = config("notion_token")
    base_url = config("base_url")
    deta_key = config("deta_key")
    stripe_key = config("stripe_key")



# base_page_id = str(uuid.UUID("6e90b64899424171af9975d4688d12d6"))
# notion_token = "secret_sUSp4QpPDl36tfbZzFQwEyqCOSrzirqWB13aFKepgps"
# base_url = "https://r917zp.deta.dev"
# deta_key = "b0rs4bo3_g4mpnBvW35e4XUBb5dPS8DQokmfGp3uG"
# stripe_key = "sk_test_x2b3B8YCbUOVizzq64f5wafN"