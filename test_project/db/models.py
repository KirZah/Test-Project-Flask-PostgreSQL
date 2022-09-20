# coding=utf-8

from sqlalchemy import (
    Table, Column, ForeignKey, UniqueConstraint,
    Integer, String, TIMESTAMP,
)
from sqlalchemy.orm import relationship, relation

from .database import Base


class BaseModel(Base):
    __abstract__ = True

    # id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)  # index=True
    # created_at = Column(TIMESTAMP, nullable=False)
    # updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


link_table = Table(
    "link_table",
    Base.metadata,
    Column("id_author", ForeignKey("authors.id_author"), primary_key=True),
    Column("id_book", ForeignKey("books.id_book"), primary_key=True),
)


class Author(BaseModel):
    __tablename__ = 'authors'

    id_author = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name_author = Column(String(255), nullable=False)

    books = relationship(
        "Book", secondary=link_table, back_populates='authors'
    )


class Book(BaseModel):
    __tablename__ = 'books'

    id_book = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name_book = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    count = Column(Integer, nullable=False)

    authors = relationship(
        "Author", secondary=link_table, back_populates='books'
    )

