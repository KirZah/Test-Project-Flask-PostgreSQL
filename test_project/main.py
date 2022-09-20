from flask import Flask, request
from loguru import logger as log

# from main import app
from test_project.db import schemas, models, crud
from test_project.db.database import SessionLocal
from test_project.models.request import GetBooksRequest

"""
todo:
Функции сервиса:
•  выдача списка книг с писателями и количеством экземпляров книг
•  фильтрация списка книг по году издания
•  добавление новой книги любого писателя (учесть, что писателя добавляемой книги в БД может не существовать)
•  удаление книги
* усложненный вариант

done:
•  выдача списка писателей (* с количеством экземпляров книг каждого автора, находящихся в БД на текущий момент)

"""

# create the extension
# create the app
app = Flask(__name__)
# # configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
import test_project.routes


@app.route("/")
def index():
    return "Index page"


@app.route('/authors', methods=['GET'])
def get_authors():
    with SessionLocal() as db:
        authors = crud.get_all_authors(db)

        log.debug(f"{authors=}")
    return authors


# @app.route('/books', methods=['GET'])
# def get_books():
#     with SessionLocal() as db:
#         books = crud.get_all_books(db)
#         log.debug(f"{books=}")
#     return books


@app.route('/books_filter', methods=['GET'])
def get_books():
    if request.method == 'GET':
        print(f"{request=}")
        request_json = request.json
        print(f"{req=}")
        request = GetBooksRequest(**request_json)

        # todo ask есть ли ограничения на то какие года допустимы
        if request.min_year is None and request.max_year is None:
            with SessionLocal() as db:
                books = crud.get_all_books(db)
                log.debug(f"{books=}")
        else:
            with SessionLocal() as db:
                books = crud.get_books_filter_by_year(
                    db=db,
                    min_year=request.min_year,
                    max_year=request.max_year,
                )
                log.debug(f"{books=}")
        return books


if __name__ == "__main__":
    app.run(debug=True)
