from fastapi import Request, FastAPI
from CommerceApi import Counter
from CommerceApi.utils.database import DetaBase
from CommerceApi.Notion.create_cms import CMSBuilder
from CommerceApi.Notion.manager import  NotionClient
from CommerceApi.Notion.timers import update_products, swap_access_keys
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from CommerceApi.routers import products, cdn
import logging
import asyncio
import os
import json

logging.error('tying to run')


try:
    from deta import Deta, App
    app = App(FastAPI())

    @app.lib.cron()
    def cron_job(event):
        print("loop")
        loop = asyncio.get_event_loop()
        print('cms')
        build = CMSBuilder()
        print('test build cms')
        loop.run_until_complete(build.maybe_create_cms())
        print('product update')
        loop.run_until_complete(update_products())
        print("updated image load logic")
        loop.run_until_complete(swap_access_keys())

except:
    from fastapi_utils.tasks import repeat_every
    app = FastAPI()

    # @app.on_event("startup")
    # async def startup_event():
    #     print("starting")
    #     build = CMSBuilder()
    #     await build.maybe_create_cms()

    # @app.on_event("startup")
    # @repeat_every(seconds=5, wait_first=True)
    # async def populate_products():
    #     print("Population products")
    #     await update_products()
    #     await swap_access_keys()

config_client = DetaBase("notion_config")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(cdn.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/product/{id}")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cart")
async def cart(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products")
async def products(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/manage_image/load/{idd}")
async def load_image(idd: str, request: Request):
    data = await config_client.get("access_keys")
    current = data.get("current_key")
    last = data.get("last_key")
    if idd == current or idd == last:
        return templates.TemplateResponse("index.html", {"request": request})
    return "error"


