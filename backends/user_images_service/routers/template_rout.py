from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



templatesapp = APIRouter(
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

@templatesapp.get('/',response_class=HTMLResponse)
def get_homepage(request: Request):
    return templates.TemplateResponse("pages/homepage.html", {"request": request})