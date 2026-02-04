from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sqlalchemy import select

from app.database.engine import SessionDep, create_db, drop_db
from app.database.models import BookModel


app = FastAPI()


class BookAddSchema(BaseModel):
    title: str
    author: str

class BookGetSchema(BookAddSchema):
    id: int


@app.post('/books')
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )

    session.add(new_book)
    await session.commit()
    return {'ok': True}


@app.get('/books')
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.post('/setup_database')
async def setup_db():
    await drop_db()
    await create_db()
    return {'ok': True}


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)