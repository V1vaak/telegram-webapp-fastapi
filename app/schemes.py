from pydantic import BaseModel


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookGetSchema(BookAddSchema):
    id: int