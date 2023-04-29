import logging

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

logging.basicConfig(
    filename="./logs/api.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

PROCESS_SERVER_URL = "http://process-server/"


class DataModel(BaseModel):
    task_id: str
    result: dict


@app.get("/")
def main():
    logger.info("プロセスサーバにAPI通信します")
    response = requests.post(
        PROCESS_SERVER_URL, json={"field1": "hoge", "field2": "piyo"}
    )
    logger.info(f"レスポンス: {response.json()}")

    return response.json()


@app.post("/callback")
async def callback_handler(request: DataModel):
    logger.info("コールバックを受信しました")
    logger.info(f"data: {request}")
    logger.info(f"task_id={request.task_id}のデータに対して処理を行う")
