from database import engine
from models.users_model import User


async def create_tables():

    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
