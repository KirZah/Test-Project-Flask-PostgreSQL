from typing import Optional, Type, Any, Dict, List

from pydantic import BaseModel, root_validator, validator


class AuthorModel(BaseModel):
    id: int
    name_author: str


class GetAuthorResponse(AuthorModel):
    books_instances_n: int


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
