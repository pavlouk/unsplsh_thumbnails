from fastapi import FastAPI
from starlette.config import Config

config = Config(".env")
ACCESS_KEY = config("ACCESS_KEY")
app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}
