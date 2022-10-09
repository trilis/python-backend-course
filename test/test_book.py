import pytest

from src.model import QueueModel
from src.db import Db


@pytest.fixture
def test_db():
    return Db(dict(), dict(), dict())


def test_book_simple(test_db):
    db = test_db
    model = QueueModel(db)
    id = model.book("Name", "K")
    assert db.has_appointment(id)
    assert db.get_appointment(id) == "Name"


def test_fresh_ids(test_db):
    model = QueueModel(test_db)
    ids = set()
    for _ in range(100):
        id = model.book("Name", "K")
        assert not (id in ids)
        ids.add(id)
