from hashlib import md5
import time


class Model:
    def execute(self, request: str) -> str:
        time.sleep(len(request) / 10)
        return md5(request.encode()).hexdigest()
