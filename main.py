from fastapi import FastAPI, Depends

import uvicorn

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import create_db, drop_db, get_session
from app.database.models import BookModel

from app.schemes import BookGetSchema, BookAddSchema


app = FastAPI()


@app.post('/books')
async def add_book(
    data: BookAddSchema, 
    session: AsyncSession = Depends(get_session)
    ) -> dict:
    new_book = BookModel(
        title=data.title,
        author=data.author
    )

    session.add(new_book)
    await session.commit()
    return {'ok': True}


@app.get('/books')
async def get_books(
    session: AsyncSession = Depends(get_session)
    ) -> list[BookGetSchema]:

    query = select(BookModel)
    result = await session.execute(query)

    return result.scalars().all()


@app.get('/books/{id}')
async def get_book(
    id: int,
    session: AsyncSession = Depends(get_session)
    ) -> BookGetSchema:

    query = select(BookModel).where(BookModel.id==id)
    result = await session.execute(query)

    return result.scalar()


@app.post('/reset_database')
async def reset_db() -> dict:
    await drop_db()
    await create_db()
    return {'ok': True}


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)