import sys

from fastapi import FastAPI

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def read_root():
    message = f"Hello world! From DevOps with Gunicorn from Uvicorn (insert unicorn emoji here)! Using Python {version}"
    return {"message": message}
