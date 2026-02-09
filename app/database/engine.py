# from typing import Annotated

# from fastapi import Depends

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.database.models import Base


engine = create_async_engine('sqlite+aiosqlite:///books.db')

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# SessionDep = Annotated[AsyncSession, Depends(get_session)]