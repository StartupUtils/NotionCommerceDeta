from CommerceApi.Notion import content, orders, products
from CommerceApi.Notion.manager import NotionClient
from CommerceApi.config import Config
from CommerceApi.utils.database import DetaBase
from CommerceApi.utils.access_key import AccessKey
import time


class BuildStep:
    def __init__(self, method, *args):
        self.method = method
        self.args = args
        self.callback = None

    async def execute(self):
        result = self.method(*self.args)
        if self.callback:
            await self.callback(result)


class CMSBuilder:
    def __init__(self):
        self.db_client = DetaBase("notion_config")
        self.base_page_id = Config.base_page_id
        self.build_queue = []
        self.TABLE = "component_config"
        self.parent = {"type": "page_id", "page_id": self.base_page_id}
        self.keys = None

    async def maybe_create_cms(self) -> None:
        built = await self.cms_already_built()
        print('built res', built)
        if built is False:
            await self.build()
        else:
            print("cms built")

    async def cms_already_built(self) -> bool:
        result = await self.db_client.find_one({"parent_id": self.base_page_id})
        print('is built', result)
        if result is None:
            return False
        return True

    async def build(self):
        self.create_order_block()
        self.create_order_table()
        self.create_product_block()
        self.create_product_table()
        self.create_image_manager()
        for command in self.build_queue:
            time.sleep(0.3)
            await command.execute()

    def create_order_block(self):
        data = content.order_content_block
        method = NotionClient.append_block_children
        self._add_build_step(method, self.base_page_id, data)

    def create_product_block(self):
        data = content.product_content_block
        method = NotionClient.append_block_children
        self._add_build_step(method, self.base_page_id, data)

    def create_order_table(self):
        data = orders.orders_schema(self.parent)
        method = NotionClient.create_database
        build_step = self._add_build_step(method, data)
        build_step.callback = self.handle_order_callback

    def create_product_table(self):
        data = products.products_schema(self.parent)
        method = NotionClient.create_database
        build_step = self._add_build_step(method, data)
        build_step.callback = self.handle_product_callback

    def create_image_manager(self):
        access = AccessKey()
        keys = access.create_keys()
        self.keys = keys
        data = content.image_manager_content_block(keys['current_key'])
        method = NotionClient.append_block_children
        build_step = self._add_build_step(method, self.base_page_id, data)
        build_step.callback = self.handle_test

    async def handle_test(self, result):
        results = result.json()['results']
        image_upload_id = results[1].get("id")
        display_id = results[2].get("id")
        keys = self.keys
        keys["upload_id"] = image_upload_id
        keys["display_id"] = display_id
        await self.db_client.insert(keys)

    def _add_build_step(self, method, *args):
        step = BuildStep(method, *args)
        self.build_queue.append(step)
        return step

    async def handle_order_callback(self, result):
        component = "order_database"
        data = self.format_payload(result, component)
        await self.db_client.insert(data)

    async def handle_product_callback(self, result):
        component = "product_database"
        data = self.format_payload(result, component)
        await self.db_client.insert(data)

    @staticmethod
    def format_payload(result, component):
        data = result.dict()
        data["key"] = component
        data["parent_id"] = result.parent.id
        data["last_updated"] = result.created_time
        return data
