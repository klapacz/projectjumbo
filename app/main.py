from fastapi import FastAPI, Response
from .db import users, todos
from passlib.hash import bcrypt
from pydantic import BaseModel
from jose import jwt
from dotenv import dotenv_values

ALGORITHM = "HS256"

config = dotenv_values(".env")
app = FastAPI()

class Credentials(BaseModel):
    name: str
    password: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(credentials: Credentials, response: Response):
    # users.getBy returns list of matching users
    user = users.getBy({"name": credentials.name})

    if len(user) == 0:
        response.status_code = 403
        return {"error": "bad username or password"}

    user = user[0]

    if not bcrypt.verify(credentials.password, user["password"]):
        response.status_code = 403
        return {"error": "bad username or password"}

    token = jwt.encode({"name": user["name"], "id": user["id"]}, config["SECRET_KEY"], algorithm=ALGORITHM)

    return token