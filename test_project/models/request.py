from typing import Optional, Type, Any, Dict

from pydantic import BaseModel, root_validator, validator

# fixme ask constraints
MIN_YEAR = -3000
MAX_YEAR = 3000


class GetBooksRequest(BaseModel):
    min_year: Optional[int]
    max_year: Optional[int]

    class Config:
        allow_mutation = False

    @staticmethod
    def _validate_year(value):
        min_year = MIN_YEAR
        max_year = MAX_YEAR
        if value < min_year or value > max_year:
            raise ValueError(
                f"Year should be in constraints "
                f"({max_year},{max_year}). Got: {value}"
            )
        return value

    @validator('min_year', pre=True)
    def validate_min_year(cls, value):
        if value is None:
            value = MIN_YEAR
        return cls._validate_year(value)

    @validator('max_year', pre=True)
    def validate_max_year(cls, value):
        if value is None:
            value = MAX_YEAR
        return cls._validate_year(value)

    @root_validator()
    def validate(cls, values):
        min_year = values.get('min_year')
        max_year = values.get('max_year')
        if min_year > max_year:
            raise ValueError(
                f"Parameter 'min_year' must be smaller for equal to "
                f"'max_year': ({min_year} > {max_year})"
            )
        return values
