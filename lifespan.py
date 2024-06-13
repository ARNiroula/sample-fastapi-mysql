from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database Connected!")

    yield

    await close_db()
    print("Database Connection Closed!")
    print("lifespan stopped")
