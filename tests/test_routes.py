import requests

SERVER_ADDRESS = 'http://127.0.0.1:5000'


def test_get_books():
    response = requests.get(
        url="http://127.0.0.1:5000/books_filter",
        json={
            'min_year': 100,
            'max_year': 300,
        }
    )
    print(f"{response=}")


test_get_books()
