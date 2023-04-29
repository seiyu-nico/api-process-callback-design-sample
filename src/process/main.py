import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
executor = ThreadPoolExecutor()

logging.basicConfig(
    filename="./logs/process.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
CALLBACK_URL = "http://api-server/callback"


class DataModel(BaseModel):
    field1: str
    field2: str


@app.post("/")
async def start_process(request: DataModel):
    logger.info("プロセスサーバにリクエストを受信しました")
    task_id = str(uuid.uuid4())  # タスクIDを生成
    logger.info(f"task_id: {task_id}")
    executor.submit(processing, task_id)

    logger.info("レスポンスを返却")
    return {"task_id": task_id, **request.dict()}  # タスクIDを返す


def processing(task_id):
    logger.info("タスク実行開始")
    time.sleep(10)  # 重たい処理の代わりに10秒待機
    result = {"hoge": "piyo"}
    logger.info("タスク実行完了")
    logger.info("コールバック呼び出し開始")
    # 処理が終わったら、コールバックURLに結果を送信
    requests.post(CALLBACK_URL, json={"task_id": task_id, "result": result})
    logger.info("コールバック呼び出し完了")
