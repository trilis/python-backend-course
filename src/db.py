from typing import Mapping


class Db:
    def __init__(
        self,
        appointments: Mapping[str, str],
        queues_ids: Mapping[str, int],
        cancelled: Mapping[str, str],
    ) -> None:
        self.appointments = appointments
        self.queues_ids = queues_ids
        self.cancelled = cancelled

    def generate_fresh_id(self, service_code: str) -> str:
        if not (service_code in self.queues_ids):
            self.queues_ids[service_code] = 1
        id = service_code + str(self.queues_ids[service_code])
        self.queues_ids[service_code] += 1
        return id

    def has_appointment(self, key: str) -> bool:
        return key in self.appointments

    def add_appointment(self, key: str, value: str) -> None:
        self.appointments[key] = value

    def delete_appointment(self, key: str) -> None:
        self.appointments.pop(key)

    def get_appointment(self, key: str) -> str:
        return self.appointments[key]

    def has_cancelled(self, key: str) -> bool:
        return key in self.cancelled

    def add_cancelled(self, key: str, value: str) -> None:
        self.cancelled[key] = value

    def get_cancelled(self, key: str) -> str:
        return self.cancelled[key]
