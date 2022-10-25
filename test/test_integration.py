from fastapi.testclient import TestClient
import pytest
import time
from hashlib import md5
from src.main import app


@pytest.mark.parametrize(
    "req", ["AAAAAAAAA", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", " "]
)
def test_request(req):
    client = TestClient(app)

    response = client.post("/request/" + req)
    assert response.status_code == 200

    id = response.json()["id"]
    assert response.json() == {"id": id}

    time.sleep(len(req) / 10 + 0.2)

    response = client.get("/check/" + id)
    assert response.status_code == 200
    assert response.json() == {
        "ready": True,
        "result": md5(req.encode()).hexdigest(),
    }
