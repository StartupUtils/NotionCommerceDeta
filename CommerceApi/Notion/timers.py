from CommerceApi.models.notion import BlockManager, ProductProperties, NotionObject
from CommerceApi.utils.database import DetaBase
from CommerceApi.Notion.manager import NotionClient
from CommerceApi.Notion.content import example_product_page
from CommerceApi.config import Config
import time

product_client = DetaBase("products")
config_client = DetaBase("notion_config")


class QueryManger:
    def __init__(self, database_id, last_updated, query={}):
        self.results = NotionClient.query_database(database_id, query)
        self.last_updated = last_updated

    @property
    def ok(self):
        if self.results.ok:
            return True
        return False

    def timed_parse(self):
        data = self.results.json()
        if "results" in data:
            for obj in data["results"]:
                
                formated_obj = NotionObject(**obj)
                properties = formated_obj.properties
                time.sleep(0.2)
                page_info_res = NotionClient.get_block_children(formated_obj.id)
                
                if page_info_res.ok:
                    pr = page_info_res.json()["results"]
                    page_info = BlockManager(pr)
                    page_info.populate_blocks()
                    self.last_updated = formated_obj.last_edited_time
      
                    yield ProductProperties(
                        id=formated_obj.id,
                        selling_section=page_info.selling_blocks,
                        more_info_section=page_info.more_info_blocks,
                        page_results=pr,
                        **properties,
                    )

                else:
                    yield
        else:
            yield


def update_product(page_id, title):
    props = {
        "properties": {
            "url (auto generated)": {
                "url": f"{Config.base_url}/product/{page_id}:title"
            }
        }
    }
    NotionClient.update(page_id, props, "pages")
    NotionClient.append_block_children(page_id, example_product_page)

def uncheck_update(page_id, title):
    props = {
        "properties": {
            "url (auto generated)": {
                "url": f"{Config.base_url}/product/{page_id}:title"
            },
            "update": {
                "checkbox": False
            }
        }
    }
    NotionClient.update(page_id, props, "pages")


async def update_products():
    try:
        query = {"component_name": "product_database"}
        product_database = await config_client.get("product_database")
        last_updated = product_database.get("last_updated")
        database_id = product_database.get("id")
        filtr = {
            "filter": {
                "or": [
                    {
                        "property": "update",
                        "checkbox": {"equals": True},
                    },
                ]
            },
            "sorts": [{"property": "updated", "direction": "ascending"}],
        }
        manage = QueryManger(database_id, last_updated, filtr)
        print(manage.results.json())
        if manage.ok:
            for product in manage.timed_parse():
                if len(product.page_results) == 0:
                    update_product(product.id, product.title)
                print(product.page_results)
                await product_client.insert(product.prep_for_insert())
                uncheck_update(product.id, product.title)
            await config_client.update({"last_updated": manage.last_updated}, "product_database")
    except Exception as e:
        print(e)
