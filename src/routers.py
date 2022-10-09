from fastapi import APIRouter

from src.model import QueueModel

router = APIRouter()
model = QueueModel()


@router.post("/book/")
async def book(name: str, service_code: str):
    id = model.book(name, service_code)
    return {"queue_id": id}


@router.post("/cancel/{id}")
async def cancel(id: str):
    model.cancel(id)
    return {}


@router.get("/check/{id}")
async def check(id: str):
    check_msg = model.check(id)
    return {"message": check_msg}
