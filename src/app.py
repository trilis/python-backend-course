import uvicorn
from fastapi import FastAPI

from src.routers import router

app = FastAPI(
    title="Queue",
    description=("tiny appointment system"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)
