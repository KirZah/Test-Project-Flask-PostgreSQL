import time
from pprint import pprint
from typing import List

import requests

from test_project.db import schemas
from test_project.models import request_models


SERVER_ADDRESS = 'http://127.0.0.1:5000'


def test_get_authors():
    response = requests.get(
        url="http://127.0.0.1:5000/authors"
    )
    print(f"{response=}")
    response: dict = response.json()['authors']
    pprint(response)


def test_get_books(min_year=None, max_year=None):
    time.sleep(0.3)
    response = requests.get(
        # url=f"http://127.0.0.1:5000/books?min_year={min_year}&max_year={max_year}",
        url="http://127.0.0.1:5000/books",
        json={
            'min_year': min_year,
            'max_year': max_year,
        }
    )

    print(f"{response=}")
    response: dict = response.json()['books']
    pprint(response)


def test_add_book(
        book: schemas.BookBase,
        authors: List[schemas.AuthorBase],
) -> None:
    time.sleep(0.5)
    add_book_request = request_models.AddBookRequest(
        book=book,
        authors=authors,
    )

    response = requests.post(
        url="http://127.0.0.1:5000/add_book",
        json=add_book_request.dict()
    )
    print(f"{response=}")
    print(f"{response.text=}")


def test_delete_book(
        id_book: int,
) -> None:
    time.sleep(0.5)
    response = requests.delete(
        url="http://127.0.0.1:5000/delete_book",
        json={
            'id_book': id_book,
        }
    )
    print(f"{response=}")
    print(f"{response.text=}")


def add_some_books():
    test_add_book(
        book=schemas.BookBase(
            name_book="Одноэтажная Америка",
            count=1,
            year=1999,  # Optional
        ),
        authors=[
            schemas.AuthorBase(name_author="Илья Ильф"),
            schemas.AuthorBase(name_author="Евгений Петров"),
        ]
    )
    test_add_book(
        book=schemas.BookBase(
            name_book="Одноэтажная Америка 2",
            count=1,
            year=1999,  # Optional
        ),
        authors=[
            schemas.AuthorBase(name_author="Илья Ильф"),
            schemas.AuthorBase(name_author="Евгений Петров"),
            schemas.AuthorBase(name_author="Новый Автор"),  # Новый автор добавился!
        ]
    )
    test_add_book(
        book=schemas.BookBase(
            name_book="Одноэтажная Америка 3",
            count=3,
            # year=1999,  # Optional
        ),
        authors=[
            schemas.AuthorBase(name_author="Вор Франшизы"),  # Такого автора нет
        ]
    )
    test_add_book(
        book=schemas.BookBase(
            name_book="Одноэтажная Америка 3",
            count=3,
            year=2003,  # Optional
        ),
        authors=[
            schemas.AuthorBase(name_author="Илья Ильф"),  # оригинальные авторы вернулись!
            schemas.AuthorBase(name_author="Евгений Петров"),  # оригинальные авторы вернулись!
        ]
    )
    test_add_book(
        book=schemas.BookBase(
            name_book="Двухэтажная Америка!",
            count=55,
            year=2005,  # Optional
        ),
        authors=[
            schemas.AuthorBase(name_author="Вор Франшизы"),  # Решил делать пародии книг
        ]
    )


if __name__ == '__main__':
    # add_some_books()
    # удаляем книжки мошенника укравшего франшизу уже дважды!
    # for i in range(26, 47):
    #     test_delete_book(id_book=i)  # todo make it 3
    # test_delete_book(id_book=5)  # todo make it 5

    test_get_authors()

    # фильтрация списка книг по году издания
    test_get_books()
    test_get_books(1999, 1999)
    test_get_books(max_year=2003)
    test_get_books(min_year=2003)
