from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.settings import settings

templatesapp = APIRouter(
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")


@templatesapp.get('/', response_class=HTMLResponse)
def get_homepage(request: Request):
    return templates.TemplateResponse(
        "pages/homepage.html", {
            "request": request,
            "id_client_google":settings.id_client_google,
            "secret_key_google_auth":settings.secret_key_google_auth
            }
        )
