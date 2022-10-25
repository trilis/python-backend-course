import time


class Model:
    def execute(self, request: str) -> int:
        time.sleep(len(request) / 10)
        return hash(request)
