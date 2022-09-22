from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel


class LinkTableBase(BaseModel):
    id_author: int
    id_book: int


class LinkTableCreate(LinkTableBase):
    pass


class LinkTable(LinkTableBase):
    author: 'Author'
    book: 'Book'


class AuthorBase(BaseModel):
    name_author: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id_author: int

    books: List[LinkTable]


class BookBase(BaseModel):
    name_book: str
    count: int
    year: Optional[int]


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id_book: int

    authors: List[LinkTable]

