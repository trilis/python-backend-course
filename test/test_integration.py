from fastapi.testclient import TestClient
import pytest

from src.app import app


def test_book_check():
    client = TestClient(app)
    response = client.get("/check/X1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "We can't find appointment with ID X1"
        + "Please check your ID or try to book an apointment again"
    }
    response = client.post("/book/?name=Petya&service_code=X")
    assert response.status_code == 200
    assert response.json() == {"queue_id": "X1"}
    response = client.get("/check/X1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Dear Petya, your appointment X1 is valid."
    }


def test_book_cancel():
    client = TestClient(app)
    response = client.post("/book/?name=Vanya&service_code=K")
    assert response.status_code == 200
    assert response.json() == {"queue_id": "K1"}
    response = client.post("/cancel/K1")
    assert response.status_code == 200
    response = client.get("/check/K1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Dear Vanya, your appointment K1 is successfully cancelled."
    }


def test_multi_cancel():
    client = TestClient(app)
    response = client.post("/book/?name=GALINA&service_code=T")
    assert response.status_code == 200
    assert response.json() == {"queue_id": "T1"}
    for _ in range(10):
        response = client.post("/cancel/T1")
        assert response.status_code == 200
        response = client.get("/check/T1")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Dear GALINA, your appointment"
            + "T1 is successfully cancelled."
        }


@pytest.mark.parametrize("id", ["K", "K100", "-T-", "#%^%&$", "1"])
def test_check_unexisting(id):
    client = TestClient(app)
    response = client.get("/check/{id}")
    assert response.status_code == 200
    assert response.json() == {
        "message": "We can't find appointment with ID {id}."
        + "Please check your ID or try to book an apointment again"
    }
