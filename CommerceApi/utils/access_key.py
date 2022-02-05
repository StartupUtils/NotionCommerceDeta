from datetime import datetime, timezone
from uuid import uuid4
from CommerceApi.config import Config


class AccessKey:
    eight_hours = 28800000
    keys = None

    def create_keys(self):
        return {
            "key": "access_keys",
            "updated": self.epoch_now,
            "current_key": str(uuid4()),
            "last_key": str(uuid4())
        }
    
    def swap_keys(self, key: dict):
        key["last_key"] = key["current_key"]
        key["current_key"] = str(uuid())
        key["updated"] = self.epoch_now
        return key

    def maybe_swap(self, key: dict):
        if (self.epoch_now - key["updated"]) > self.eight_hours:
            key = self.swap_keys(key)
        self.keys = key
        return key
    
    @property
    def epoch_now(self):
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    def create_url(self, path):
        return f"{Config.base_url}/manage_image/{path}/{self.keys.get('current_key')}"

    @property
    def image_upload_obj(self):
        return {
            "embed": {"url": self.create_url("load")}
        }

    @property
    def image_display_obj(self):
        return {
            "embed": {"url": self.create_url("show")}
        }




