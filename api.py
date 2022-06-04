from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_bot():
    return {"Hello": "World"}

