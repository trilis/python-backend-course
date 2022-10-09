from fastapi.testclient import TestClient
import pytest

from src.app import app

@pytest.mark.parametrize("name,code", [("Petya", "X")])
def test_book_check(name, code):
    client = TestClient(app)
    expected_id = code + "1"
    response = client.get("/check/" + expected_id)
    assert response.status_code == 200
    assert response.json() == {
        "message": "We can't find appointment with ID " + expected_id
        + ". Please check your ID or try to book an apointment again"
    }
    response = client.post("/book/?name=" + name + "&service_code=" + code)
    assert response.status_code == 200
    assert response.json() == {"queue_id": expected_id}
    response = client.get("/check/" + expected_id)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Dear " + name + ", your appointment " + expected_id + " is valid."
    }


@pytest.mark.parametrize("name,code", [("Vanya", "K")])
def test_book_cancel(name, code):
    client = TestClient(app)
    response = client.post("/book/?name=" + name + "&service_code=" + code)
    expected_id = code + "1"
    assert response.status_code == 200
    assert response.json() == {"queue_id": expected_id}
    response = client.post("/cancel/" + expected_id)
    assert response.status_code == 200
    response = client.get("/check/" + expected_id)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Dear " + name + ", your appointment " + expected_id + " is successfully cancelled."
    }


@pytest.mark.parametrize("name,code", [("GALINA", "T")])
def test_multi_cancel(name, code):
    client = TestClient(app)
    response = client.post("/book/?name=" + name + "&service_code=" + code)
    expected_id = code + "1"
    assert response.status_code == 200
    assert response.json() == {"queue_id": expected_id}
    for _ in range(10):
        response = client.post("/cancel/" + expected_id)
        assert response.status_code == 200
        response = client.get("/check/" + expected_id)
        assert response.status_code == 200
        assert response.json() == {
            "message": "Dear " + name + ", your appointment "
            + expected_id + " is successfully cancelled."
        }


@pytest.mark.parametrize("id", ["K", "K100", "-T-", "1"])
def test_check_unexisting(id):
    client = TestClient(app)
    response = client.get("/check/" + id)
    assert response.status_code == 200
    assert response.json() == {
        "message": "We can't find appointment with ID " + id
        + ". Please check your ID or try to book an apointment again"
    }
