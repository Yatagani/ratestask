import pytest 
from requests import get


def test_incorrect_origin_parameter():

    params = {
        'date_from': '2016-01-01',
        'date_to': '2016-01-10',
        'origin': 'asd',
        'destination': 'north_europe_main'
    }

    result = get("http://localhost/rates", params=params)

    assert result.status_code == 400
    assert result.json() == {"error": f"{params['origin']} does not exist in the database"}


def test_incorrect_date_format_parameter():

    # Checks if date format is YYYY-MM-DD

    params = {
        'date_from': '2016-01-01s',
        'date_to': '2016-01-10',
        'origin': 'CNSGH',
        'destination': 'north_europe_main'
    }

    result = get("http://localhost/rates", params=params)

    assert result.status_code == 400
    assert result.json() == {"error": f"'{params['date_from']}' is not a 'date'"}


def test_empty_parameter():

    params = {
        'date_from': '2016-01-01',
        'date_to': '2016-01-10',
        'origin': '',
        'destination': 'north_europe_main'
    }

    result = get("http://localhost/rates", params=params)

    assert result.status_code == 400
    assert result.json() == {"error": f"{params['origin']} does not exist in the database"}


def test_prices_fetched_correctly():

    params = {
        'date_from': '2016-01-01',
        'date_to': '2016-01-10',
        'origin': 'CNSGH',
        'destination': 'north_europe_main'
    }

    expected_result = [
        {
            "day": "2016-01-01",
            "average_price": 1112
        },
        {
            "day": "2016-01-02",
            "average_price": 1112
        },
        {
            "day": "2016-01-04",
            "average_price": None
        },
        {
            "day": "2016-01-05",
            "average_price": 1142
        },
        {
            "day": "2016-01-06",
            "average_price": 1142
        },
        {
            "day": "2016-01-07",
            "average_price": 1137
        },
        {
            "day": "2016-01-08",
            "average_price": 1124
        },
        {
            "day": "2016-01-09",
            "average_price": 1124
        },
        {
            "day": "2016-01-10",
            "average_price": 1124
        }
    ]
    result = get("http://localhost/rates", params=params)

    assert result.status_code == 200
    assert result.json() == expected_result
