from typing import Optional, Type, Any, Dict, List

from pydantic import BaseModel, root_validator, validator

from test_project.db.schemas import BookBase, AuthorBase

# todo: ask year constraints
MIN_YEAR = -3000
MAX_YEAR = 3000


class GetBooksRequest(BaseModel):
    min_year: Optional[int]
    max_year: Optional[int]

    class Config:
        allow_mutation = False

    @validator('min_year', 'max_year', pre=True)
    def validate_year(cls, value):
        if value is None:
            return value

        min_year = MIN_YEAR
        max_year = MAX_YEAR
        if value < min_year or value > max_year:
            raise ValueError(
                f"Year should be in constraints "
                f"({max_year},{max_year}). Got: {value}"
            )
        return value

    @root_validator()
    def validate(cls, values):
        min_year = values.get('min_year')
        max_year = values.get('max_year')

        if min_year is None or max_year is None:
            return values

        if min_year > max_year:
            raise ValueError(
                f"Parameter 'min_year' must be smaller for equal to "
                f"'max_year': ({min_year} > {max_year})"
            )
        return values


class AddBookRequest(BaseModel):
    book: BookBase
    authors: List[AuthorBase]
