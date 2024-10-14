from fastapi import FastAPI, Path, HTTPException, status, Body, Request, Form
from fastapi.responses import HTMLResponse
# from typing import Annotated
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory='templates')  # объект класса Jinja2Templates
users = []


class User(BaseModel):
    id: int = 0
    username: str = 'Master'
    age: int = 99


@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get("/user/{user_id}")
def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users[user_id]})


@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: Request, username: str = Form(), age: str = Form()) -> HTMLResponse:
    # user_id = len(users)+1
    # user.username = username
    # user.age = age
    if users:
        user_id = max(users, key=lambda m: m.id).id + 1
    else:
        user_id = 0
    users.append(User(id=user_id, username=username, age=age))
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.put('/user/{id}/{username}/{age}')
def update_user(id: int, username: str, age: int, user: User = Body()) -> User:
    try:
        edit_user = users[id-1]
        edit_user.username = username
        edit_user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{id}')
def delete_user(id: int, user: User ) -> User:
    try:
        users.pop(id-1)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


# python -m uvicorn main:app