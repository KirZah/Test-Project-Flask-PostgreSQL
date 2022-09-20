import functools
from typing import Optional, Type

from sqlalchemy import func, asc, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.dialects import postgresql
# from loguru import logger as log

from test_project.db import models, schemas

"""

•  выдача списка писателей (* с количеством экземпляров книг каждого 
        автора, находящихся в БД на текущий момент)
done:
•  выдача списка книг с писателями и количеством экземпляров книг
•  фильтрация списка книг по году издания
•  добавление новой книги любого писателя (учесть, что писателя 
        добавляемой книги в БД может не существовать)
•  удаление книги
"""


def get_all_authors(db: Session):  # List[models.Author]
    return db.query(models.Author).all()


def get_needed_author(
        db: Session,
        author_name: str,
) -> models.Author:
    # fixme should get only one author, but name_author is not unique?
    # todo ask if name_author is unique
    return db.query(models.Author) \
        .where(models.Author.name_author == author_name) \
        .one()


def get_all_books(db: Session):  # List[models.Books]
    return db.query(models.Book).all()


def get_books_filter_by_year(
        db: Session,
        min_year: int,
        max_year: int,
):  # List[models.Books]
    return db.query(models.Book) \
        .filter(min_year <= models.Book.year <= max_year) \
        .all()


def create_author(
        db: Session,
        author: schemas.AuthorCreate,
) -> models.Author:
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(
        db: Session,
        book: schemas.BookCreate,
) -> models.Author:
    db_book = models.Author(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def create_author_book_link(
        db: Session,
        id_author: int,
        id_book: int) -> models:
    db_link = models.link_table(id_author=id_author, id_book=id_book)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)

    return db_link


def delete_book(db: Session, id_book: int) -> None:
    db.query(models.Book).filter(models.Book.id_book == id_book).delete()
