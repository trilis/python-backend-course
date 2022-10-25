from fastapi.testclient import TestClient
from pymongo import MongoClient
import random
import uuid

from src.main import app


def test_check_not_ready():
    client = TestClient(app)
    db_client = MongoClient("mongodb://localhost:27017/")["results_db"]

    id = "TEST" + str(uuid.uuid4())
    db_client["results"].delete_one({"key": id})

    response = client.get("/check/" + id)
    assert response.status_code == 200
    assert response.json() == {"ready": False, "result": ""}


def test_check_ready():
    client = TestClient(app)
    db_client = MongoClient("mongodb://localhost:27017/")["results_db"]

    id = "TEST" + str(uuid.uuid4())
    value = str(random.randint(0, 10000))
    db_client["results"].insert_one({"key": id, "value": value})

    response = client.get("/check/" + id)
    assert response.status_code == 200
    assert response.json() == {"ready": True, "result": value}


def test_request_ok():
    client = TestClient(app)

    request = "TEST" + str(uuid.uuid4())

    response = client.post("/request/" + request)
    assert response.status_code == 200
    assert response.json() == {"id": response.json()["id"]}
