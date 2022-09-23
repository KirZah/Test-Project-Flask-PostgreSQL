from flask import Flask, request, Response
from sqlalchemy.orm import Session
from loguru import logger as log

from test_project.db import schemas, models, crud
from test_project.db.database import SessionLocal
from test_project.models import request_models, response_models

""" Функции сервиса

half/done:
•  выдача списка писателей (* с количеством экземпляров книг каждого автора, находящихся в БД на текущий момент)

done:
•  фильтрация списка книг по году издания
•  добавление новой книги любого писателя (учесть, что писателя добавляемой книги в БД может не существовать)
•  удаление книги
•  выдача списка книг с писателями и количеством экземпляров книг

"""

app = Flask(__name__)


@app.route("/")
def index():
    return "Index page"


@app.route('/authors', methods=['GET'])
def get_authors():
    response = response_models.GetAuthorsResponse(authors=[])
    with SessionLocal() as db:
        authors = crud.get_all_authors(db)
        for row in authors:
            author = row[0]
            response.authors.append(response_models.GetAuthorResponse(
                id=author.id_author,
                name_author=author.name_author,
            ))

    log.debug(f"{response.json() = }")

    return Response(response.json(), status=200)


@app.route('/books', methods=['GET'])
def get_books():  # todo make request with params in url
    data: dict = request.json
    log.debug(f"{request.json = }")

    req = request_models.GetBooksRequest(
        min_year=data['min_year'],
        max_year=data['max_year'],
    )
    log.debug(f"{req = }")

    response = response_models.GetBooksResponse(books=[])
    with SessionLocal() as db:
        if req.min_year is None and req.max_year is None:
            log.info(f"Trying to get books without year borders")
            books = crud.get_all_books(db)
            log.debug(f"{books=}")
        else:
            books = crud.get_books_filter_by_year(
                db=db,
                min_year=req.min_year,
                max_year=req.max_year,
            )
            log.debug(f"{books=}")

        for book in books:
            book: models.Book
            authors = crud.get_book_authors(db, id_book=book.id_book)
            authors = [
                response_models.AuthorModel(
                    id=author.id_author,
                    name_author=author.name_author,
                )
                for author in authors
            ]
            response.books.append(response_models.GetBookResponse(
                id=book.id_book,
                name_book=book.name_book,
                amount=book.count,
                year=book.year,
                authors=authors,
            ))
    log.debug(f"{response.dict() = }")

    return Response(response.json(), status=200)


@app.route('/add_book', methods=['POST'])
def add_book():  # todo make it a transaction
    data: dict = request.json
    log.debug(f"{request.json = }")
    req = request_models.AddBookRequest(**data)
    log.debug(f"{req = }")
    with SessionLocal() as db:
        db: Session

        book: models.Book = crud.create_book(
            db=db,
            book=schemas.BookCreate(**req.book.dict())
        )

        for author_base in req.authors:
            author_base: schemas.AuthorBase
            try:
                author = crud.get_author_by_name(db, author_base.name_author)
            except Exception as err:  # fixme use less wide exception
                log.error(err)
                db.rollback()
                author = crud.create_author(
                    db=db,
                    author=schemas.AuthorCreate(**author_base.dict())
                )

            crud.create_author_book_link(
                db=db,
                link_row=schemas.LinkTableCreate(
                    id_author=author.id_author,
                    id_book=book.id_book,
                )
            )

    return Response("ok", status=200)


@app.route('/delete_book', methods=['DELETE'])
def delete_book():
    data: dict = request.json
    log.debug(data)
    with SessionLocal() as db:
        crud.delete_book(db, id_book=data['id_book'])

    return Response("ok", status=200)


if __name__ == "__main__":
    app.run(debug=True)
