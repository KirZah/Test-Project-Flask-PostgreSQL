from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name_author: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id_author: int

    books: List['Book']


class BookBase(BaseModel):
    name_book: str
    year: Optional[int]
    count: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id_book: int

    authors: List['Author']
