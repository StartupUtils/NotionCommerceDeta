from fastapi import Request, FastAPI
from CommerceApi.Notion.create_cms import CMSBuilder
from CommerceApi.Notion.manager import  NotionClient
from CommerceApi.Notion.timers import update_products
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from CommerceApi.routers import products
import logging
import asyncio

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

except:
    from fastapi_utils.tasks import repeat_every
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        print("starting")
        build = CMSBuilder()
        await build.maybe_create_cms()

    @app.on_event("startup")
    @repeat_every(seconds=5, wait_first=True)
    async def populate_products():
        print("Population products")
        await update_products()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/product/{id}")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cart")
async def cart(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


