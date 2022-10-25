import pika
import json
import logging
import uuid

from src.model import Model
from src.db import Db

worker_id = str(uuid.uuid4())

logging.basicConfig()
logger = logging.getLogger(f"worker {worker_id}")
logger.setLevel(logging.INFO)

model = Model()
db = Db()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
    )
)
channel = connection.channel()

channel.queue_declare(queue="requests", durable=True)
logger.info("Starting worker...")


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    request = data["request"]
    uid = data["uid"]

    logger.info(f"[{uid}] Started request processing")
    response = model.execute(request)
    logger.info(f"[{uid}] Finished request processing")

    db.set(uid, response)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info(f"[{uid}] Done")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="requests", on_message_callback=callback)

channel.start_consuming()
