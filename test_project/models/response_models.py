from typing import Optional, List

from pydantic import BaseModel


class AuthorModel(BaseModel):
    id: int
    name_author: str


class GetAuthorResponse(AuthorModel):
    # books_instances_n: int  # todo
    ...


class GetAuthorsResponse(BaseModel):
    authors: List[GetAuthorResponse]


class GetBookResponse(BaseModel):
    id: int
    year: Optional[int]
    name_book: str
    amount: int
    authors: List[AuthorModel]


class GetBooksResponse(BaseModel):
    books: List[GetBookResponse]
