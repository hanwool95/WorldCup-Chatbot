from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class User(BaseModel):
    query: str

@app.get("/")
def read_bot():
    return {"Hello": "World"}

@app.post("/")
def post_bot(user: User):
    print(user.query)
    result = ""
    result = user.query
    result_dict = {"result": result}
    return result_dict



