import pytest
from src.db import Db
from src.model import QueueModel


@pytest.fixture
def test_db():
    return Db({"X100": "Petya"}, dict(), dict())


@pytest.mark.parametrize("name,id", [("Petya", "X100")])
def test_cancel_simple(test_db, name, id):
    model = QueueModel(test_db)
    model.cancel(id)
    assert not (test_db.has_appointment(id))
    assert test_db.has_cancelled(id)
    assert test_db.get_cancelled(id) == name


@pytest.mark.parametrize("name,id", [("Petya", "X100")])
def test_cancel_multiple(test_db, name, id):
    model = QueueModel(test_db)
    for _ in range(10):
        model.cancel(id)
        assert not (test_db.has_appointment(id))
        assert test_db.has_cancelled(id)
        assert test_db.get_cancelled(id) == name


@pytest.mark.parametrize("id", ["Y5"])
def test_cancel_nonexisting(test_db, id):
    model = QueueModel(test_db)
    model.cancel(id)
    assert not (test_db.has_appointment(id))
    assert not (test_db.has_cancelled(id))
