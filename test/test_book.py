from string import ascii_uppercase
import pytest

from src.model import QueueModel
from src.db import Db


@pytest.fixture
def test_db():
    return Db(dict(), dict(), dict())


@pytest.mark.parametrize("name,code", [("Name", "K")])
def test_book_simple(test_db, name, code):
    db = test_db
    model = QueueModel(db)
    id = model.book(name, code)
    assert db.has_appointment(id)
    assert db.get_appointment(id) == name


@pytest.mark.parametrize("name", ["Name"])
def test_book_many(test_db, name):
    db = test_db
    model = QueueModel(db)
    for i in ascii_uppercase:
        id = model.book(name, i)
        assert db.has_appointment(id)
        assert db.get_appointment(id) == name


@pytest.mark.parametrize("name,code", [("Name", "K")])
def test_fresh_ids(test_db, name, code):
    model = QueueModel(test_db)
    ids = set()
    for _ in range(100):
        id = model.book(name, code)
        assert not (id in ids)
        ids.add(id)
