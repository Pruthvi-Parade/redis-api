# This is a sample Python script.
import redis
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Allows anyone to hit the API with * you can even add localhost to only allow yourself
    allow_origins=["*"],
    # Allows us to accept all type of parameters
    allow_credentials=True,
    # Allows all methods
    allow_methods=["*"],
    # Like JWT token things we can pass any headers
    allow_headers=["*"],
    expose_headers=["*"]
)


class Items(BaseModel):
    ip: str
    command: str


@app.post("/add_panel_event", description="This does something I dont know")
def ip_command(obj: Items):
    try:
        redis_obj = redis.Redis(
            host= 'localhost',
            port= '6379'
        )
        redis_obj.set("ip", obj.ip)
        value = redis_obj.get("ip")
        redis_obj.set("command", obj.command)
        return {
            "ip": redis_obj.get("ip"),
            "command": redis_obj.get("command")
        }

        # redis_obj.zadd('vehicles', {'car': 0})
        # redis_obj.zadd('vehicles', {'bike': 0})

        # vehicles = redis_obj.zrange('vehicles', 0, -1)
        # print(vehicles)
    except Exception as e:
        logger.debug(f"{e}")
        raise e


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8888, reload=True)
