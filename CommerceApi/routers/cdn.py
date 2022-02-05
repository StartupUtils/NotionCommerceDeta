from fastapi import Request, FastAPI, File, UploadFile, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, HTMLResponse
from CommerceApi.utils.database import DETA

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

drive = DETA.CLIENT.Drive("images")


@router.get("/load", response_class=HTMLResponse)
def render():
    return """
    <form action="/images/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """


@router.post("/upload")
def upload_img(file: UploadFile = File(...)):
    name = file.filename
    f = file.file
    res = drive.put(name, f)
    return res

@router.get("/fetch/logo")
def download_img():
    res = drive.get("img.png")
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")

@router.get("/fetch/{name}")
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")


@router.get("/fetch/{name}")
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")


@router.get("/items/home", response_class=HTMLResponse)
async def home():
    res = drive.get("home.html")
    html = ""
    for chunck in res.iter_chunks(1024):
        html += chunck.decode()
    return html