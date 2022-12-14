from pydantic.error_wrappers import ValidationError

from test_project.models.request_models import GetBooksRequest
from test_project.models.request_models import MIN_YEAR, MAX_YEAR


def test_class_get_books_request():
    def test_ok_case(min_year, max_year):
        try:
            request = GetBooksRequest(
                min_year=min_year,
                max_year=max_year,
            )
        except Exception:
            raise AssertionError("Had to be ok!")
        else:
            print("'Correct params' passed")
        return request

    def test_if_mutable():
        try:
            request = GetBooksRequest(
                min_year=-30,
                max_year=2050,
            )
            request.min_year = 2022
        except TypeError as err:
            assert str(err) == '"GetBooksRequest" is immutable and does not support item assignment'
            print("'Immutable test' passed")
        else:
            raise AssertionError("Should be immutable!")

    def test_if_min_less_than_max():
        try:
            GetBooksRequest(
                min_year=2107,
                max_year=2050,
            )
        except ValidationError:
            print(f"'min smaller than max' passed!")
        else:
            raise AssertionError(f"'min smaller than max' NOT PASSED!")

    def test_year_boundaries(min_year, max_year):
        try:
            GetBooksRequest(
                min_year=min_year,
                max_year=max_year,
            )
        except ValidationError:
            print(f"'Year boundaries' passed!")
        else:
            raise AssertionError(f"'min smaller than max' NOT PASSED!")

    test_ok_case(-30, 2050)
    test_if_mutable()
    test_if_min_less_than_max()
    test_year_boundaries(MIN_YEAR - 1, MAX_YEAR)
    test_year_boundaries(MIN_YEAR, MAX_YEAR + 1)
    test_year_boundaries(MIN_YEAR - 1, MAX_YEAR + 1)


test_class_get_books_request()
