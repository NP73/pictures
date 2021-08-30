from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from config.database import metadata, engine, database

from repositories.users import *
from repositories.pictures import *

from routers.users import usersapp
from routers.pictures import pictureapp
from routers.template_rout import templatesapp
from routers.socket_route import socket_rout


origins = [
    "http://localhost:8000/",
    "http://localhost/",
    "http://api-booking.ru:8000",
    "http://api-booking.ru"
]

tags_metadata = [{
    "name": "users-api",
    "description": "Api сервиса User",
}]


app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    openapi_tags=tags_metadata,
    description="Документация API сервиса Users",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata.create_all(engine)

app.state.database = database


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    usersapp,
    tags=["users"]
)
app.include_router(
    pictureapp,
    tags=["picture"]
)

app.include_router(
    templatesapp,
    tags=["templates"]
)

app.include_router(
    socket_rout
)
