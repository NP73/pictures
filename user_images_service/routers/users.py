from fastapi import APIRouter,  Depends


from repositories.users import Users
from schemas import users
usersapp = APIRouter(
    prefix="/api/v1/users",
    responses={404: {"description": "Not found"}}
)


@usersapp.post('/')
async def create(user: users.UserCreate):
    user_get = await Users.objects.get_or_none(id_google_client=user.id_google_client)
    if not user_get:
        return await Users.objects.create(**user.dict())
    else:
        return user_get


@usersapp.get('/')
async def get_all():
    return await Users.objects.all()


@usersapp.get('/{id}')
async def get_one(id: int):
    return await Users.objects.get_or_none(id=id)

@usersapp.post('/change_status/{id}')
async def update_status_user(id: str):
    user = await Users.objects.get_or_none(id_google_client=id)
    await user.update(access = 1)
    return
