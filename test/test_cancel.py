import pytest
from src.db import Db
from src.model import QueueModel


@pytest.fixture
def test_db():
    return Db({"X100": "Petya"}, dict(), dict())


def test_cancel_simple(test_db):
    model = QueueModel(test_db)
    model.cancel("X100")
    assert not (test_db.has_appointment("X100"))
    assert test_db.has_cancelled("X100")
    assert test_db.get_cancelled("X100") == "Petya"


def test_cancel_multiple(test_db):
    model = QueueModel(test_db)
    for _ in range(10):
        model.cancel("X100")
        assert not (test_db.has_appointment("X100"))
        assert test_db.has_cancelled("X100")
        assert test_db.get_cancelled("X100") == "Petya"


def test_cancel_nonexisting(test_db):
    model = QueueModel(test_db)
    model.cancel("Y5")
    assert not (test_db.has_appointment("Y5"))
    assert not (test_db.has_cancelled("Y5"))
