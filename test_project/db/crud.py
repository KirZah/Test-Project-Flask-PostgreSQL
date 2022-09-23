import functools
from typing import Optional, Callable, List

from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from loguru import logger as log

from test_project.db import models, schemas


def _add_commit_refresh(f: Callable):

    @functools.wraps(f)
    def wrapper(db: Session, *args, **kwargs):
        db_obj = f(db, *args, **kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        log.debug(f"{db_obj=}")
        return db_obj

    return wrapper


@_add_commit_refresh
def create_author(
        db: Session,
        author: schemas.AuthorCreate,
) -> models.Author:
    return models.Author(**author.dict())


@_add_commit_refresh
def create_book(
        db: Session,
        book: schemas.BookCreate,
) -> models.Book:
    return models.Book(**book.dict())


@_add_commit_refresh
def create_author_book_link(
        db: Session,
        link_row: schemas.LinkTableCreate,
) -> models.LinkTable:
    return models.LinkTable(**link_row.dict())


def get_all_authors(db: Session) -> List[models.Author]:
    stmt = select(models.Author)
    log.debug(f"QUERY = '''\n{stmt}\n'''")
    result = db.execute(stmt)
    db.commit()
    return result


def get_author_by_name(
        db: Session,
        name_author: str,
) -> models.Author:
    # fixme should get only one author, but what if name_author is not unique?
    return db.query(models.Author) \
        .where(models.Author.name_author == name_author) \
        .one()


def get_book_authors(db: Session, id_book: int) -> List[models.Author]:
    return db.query(models.Author) \
        .join(models.LinkTable, models.LinkTable.id_author == models.Author.id_author) \
        .filter(models.LinkTable.id_book == id_book) \
        .all()


def get_all_books(db: Session) -> List[models.Book]:
    return db.query(models.Book).all()


def get_books_filter_by_year(
        db: Session,
        min_year: Optional[int],
        max_year: Optional[int],
) -> List[models.Book]:

    query = db.query(models.Book)
    if not (min_year is None):
        query = query.filter(min_year <= models.Book.year)
    if not (max_year is None):
        query = query.filter(models.Book.year <= max_year)

    return query.all()


def delete_book(db: Session, id_book: int) -> None:
    db.query(models.Book) \
        .filter(models.Book.id_book == id_book) \
        .delete()
    db.commit()
