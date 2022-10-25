import pika
import json
import uuid
import logging
from fastapi import APIRouter

from src.db import Db

logging.basicConfig()
logger = logging.getLogger("modelrequest-server")
logger.setLevel(logging.INFO)

router = APIRouter()
db = Db()


def sendMessage(request: str, uid: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="requests", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="requests",
        body=json.dumps(
            {
                "request": request,
                "uid": uid,
            }
        ),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ),
    )
    connection.close()


@router.post("/request/{req}")
async def request(req: str):
    id = str(uuid.uuid4())
    logger.info(f"[{id}] New request {req}")
    sendMessage(req, id)
    logger.info(f"[{id}] Sent to worker")
    return {"id": id}


@router.get("/check/{id}")
async def check(id: str):
    logger.info(f"[{id}] Checking request")
    if db.has(id):
        logger.info(f"[{id}] Ready, returning result")
        return {"ready": True, "result": db.get(id)}
    else:
        logger.info(f"[{id}] Not ready yet")
        return {"ready": False, "result": ""}
