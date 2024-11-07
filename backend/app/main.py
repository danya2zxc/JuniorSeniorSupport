from contextlib import asynccontextmanager

from fastapi import FastAPI
from repository import create_tables, delete_tables
from routers import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()
    print("Database cleared")
    await create_tables()
    print("Database ready")
    yield
    print("Shut down")


app = FastAPI()

app.include_router(users_router.router, prefix="/api/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "hello world"}
