from CommerceApi.models.notion import BlockManager, ProductProperties, NotionObject
from CommerceApi.utils.database import DetaBase
from CommerceApi.utils.stripe import StripeManager
from CommerceApi.Notion.manager import NotionClient
from CommerceApi.Notion.content import example_product_page
from CommerceApi.config import Config
from CommerceApi.utils.access_key import AccessKey
import time

product_client = DetaBase("products")
config_client = DetaBase("notion_config")
stripe = StripeManager(Config.stripe_key)


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

        #         else:
        #             yield
        # else:
        #     yield


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
                current_product = await product_client.get(product.id)
                # breakpoint()
                print(current_product)
                if current_product and current_product.get("product_id") and current_product.get("price_id"):
                    product_id = current_product.get("product_id")
                    price_id = current_product.get("price_id")
                    stripe_obj = stripe.update_listing(
                        product_id=product_id,
                        price_id=price_id,
                        title=product.title,
                        images=product.images,
                        price=product.price
                    )
                else:
                    stripe_obj = stripe.create_new_product(
                        title=product.title,
                        images=product.images,
                        price=product.price
                    )
                product_id, price_id = stripe_obj.product.id, stripe_obj.price.id
                product.add_stripe_info(product_id, price_id)
                await product_client.insert(product.prep_for_insert())
                uncheck_update(product.id, product.title)
            await config_client.update({"last_updated": manage.last_updated}, "product_database")
    except Exception as e:
        print(e)

async def swap_access_keys():
    data = await config_client.get("access_keys")
    access = AccessKey()
    keys = access.maybe_swap(data)
    upload_id = keys.get("upload_id")
    display_id = keys.get("display_id")
    await config_client.put(keys)
    current_product = keys.get("current_key")
    NotionClient.update_block(upload_id, access_keys.image_upload_id)
    NotionClient.update_block(display_id, access_keys.image_display_obj)



