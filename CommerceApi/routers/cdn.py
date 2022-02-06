from fastapi import Request, FastAPI, File, UploadFile, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, RedirectResponse
from CommerceApi.utils.database import DETA
from CommerceApi.config import Config
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

drive = DETA.CLIENT.Drive("images")
templates = Jinja2Templates(directory="templates")


@router.get("/load", response_class=HTMLResponse)
def render():
    return """
    <form action="/images/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """


@router.post("/upload")
def upload_img(request: Request, file: UploadFile = File(...)):
    name = file.filename
    f = file.file
    res = drive.put(name, f)
    return RedirectResponse(request.headers.get('referer'))

@router.get("/fetch/logo")
def get_logo_img():
    try:
        res = drive.get("logo.png")
        return StreamingResponse(res.iter_chunks(1024), media_type="image/png")
    except:
        return JSONResponse(status_code=404, content={"info": "No logo found"})

@router.get("/fetch/{name}")
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")

@router.get("/fetchall")
def fetchall():
    urls = []
    res = drive.list()
    for name in res.get("names"):
        url = f"{Config.base_url}/images/fetch/{name}"
        urls.append(url)

    return JSONResponse(status_code=200, content={"data": urls})
