import pytest

from src.model import QueueModel
from src.db import Db


@pytest.fixture
def test_model():
    return QueueModel(Db({"X1": "Petya"}, dict(), {"Y100": "Vanya"}))

@pytest.mark.parametrize("name,id", [("Petya", "X1")])
def test_check_ok(test_model, name, id):
    message = test_model.check(id)
    assert message == "Dear " + name + ", your appointment " + id + " is valid."


@pytest.mark.parametrize("name,id", [("Vanya", "Y100")])
def test_check_cancel(test_model, name, id):
    message = test_model.check(id)
    assert (
        message
        == "Dear " + name + ", your appointment " + id + " is successfully cancelled."
    )

@pytest.mark.parametrize("id", ["Z42"])
def test_check_fail(test_model, id):
    message = test_model.check(id)
    assert (
        message
        == "We can't find appointment with ID " + id +
        ". Please check your ID or try to book an apointment again"
    )
