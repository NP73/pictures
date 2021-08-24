from fastapi import APIRouter,  Depends


from repositories.users import Users
from schemas import users
usersapp = APIRouter(
    prefix="/api/v1/users",
    responses={404: {"description": "Not found"}}
)



@usersapp.post('/')
async def create(user: users.UserCreate):
    return await Users.objects.create(**user.dict())
    

  

@usersapp.get('/')
async def get_all():
    return await Users.objects.all()


@usersapp.get('/{id}')
async def get_one(id:int):
    return await Users.objects.get_or_none(id=id)
