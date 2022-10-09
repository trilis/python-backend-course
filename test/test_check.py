import pytest

from src.model import QueueModel
from src.db import Db


@pytest.fixture
def test_model():
    return QueueModel(Db({"X1": "Petya"}, dict(), {"Y100": "Vanya"}))


def test_check_ok(test_model):
    message = test_model.check("X1")
    assert message == "Dear Petya, your appointment X1 is valid."


def test_check_cancel(test_model):
    message = test_model.check("Y100")
    assert (
        message
        == "Dear Vanya, your appointment Y100 is successfully cancelled."
    )


def test_check_fail(test_model):
    message = test_model.check("Z42")
    assert (
        message
        == "We can't find appointment with ID Z42."
        + "Please check your ID or try to book an apointment again"
    )
