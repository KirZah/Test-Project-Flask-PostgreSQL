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
        # return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
        return "<{0.__class__.__name__}()>".format(self)


class Author(BaseModel):
    __tablename__ = 'authors'

    id_author = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name_author = Column(String(255), nullable=False)

    books = relationship("LinkTable", back_populates='author')


class Book(BaseModel):
    __tablename__ = 'books'

    id_book = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name_book = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    count = Column(Integer, nullable=False)

    authors = relationship("LinkTable", back_populates='book')


class LinkTable(Base):
    __tablename__ = "link_table"
    id_author = Column(ForeignKey("authors.id_author", ondelete="CASCADE"), primary_key=True)
    id_book = Column(ForeignKey("books.id_book", ondelete="CASCADE"), primary_key=True)

    author = relationship("Author", back_populates="books")
    book = relationship("Book", back_populates="authors")

