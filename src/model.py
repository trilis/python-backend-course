from src.db import Db


class QueueModel:
    def __init__(self, db: Db = None):
        if db is None:
            self.db = Db(dict(), dict(), dict())
        else:
            self.db = db

    def book(self, name: str, service_code: str) -> str:
        id = self.db.generate_fresh_id(service_code)
        self.db.add_appointment(id, name)
        return id

    def cancel(self, id: str) -> None:
        if not (self.db.has_appointment(id)):
            return
        self.db.add_cancelled(id, self.db.get_appointment(id))
        self.db.delete_appointment(id)
        return

    def check(self, id: str) -> str:
        if not (self.db.has_appointment(id)):
            if self.db.has_cancelled(id):
                name = self.db.get_cancelled(id)
                cancelled_message = (
                    "Dear "
                    + name
                    + ", your appointment "
                    + id
                    + " is successfully cancelled."
                )
                return cancelled_message
            else:
                fail_message = (
                    "We can't find appointment with ID "
                    + id
                    + ". Please check your ID"
                    + " or try to book an apointment again"
                )
                return fail_message
        name = self.db.get_appointment(id)
        ok_message = "Dear " + name + ", your appointment " + id + " is valid."
        return ok_message
