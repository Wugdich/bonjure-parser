import time
from random import uniform

import requests
from fake_useragent import UserAgent

import config


def _delay() -> None:
    """Function imitates delay and makes requests more human-like."""

    time.sleep(uniform(0.5, 1))


def get_categories_ids() -> list[int]:
    """Fucntion requests to bonjure-dv API, gets json with categroies data
    and extracts ids of smallest categories."""

    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://bonjour-dv.ru',
        'Connection': 'keep-alive',
        'Referer': 'https://bonjour-dv.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'If-None-Match': 
        'W/"0e858478c9345658abe4976a0d3f9567|43909681-d6e1-432d-b61f-ddac393cb5da"',
    }

    parse_attempts = config.PARSE_ATTEMPTES
    parse_timeout = config.PARSE_TIMEOUT
    while parse_attempts > 0:
        parse_attempts -= 1
        try:
            response = requests.get(
                    'https://api.bonjour-dv.ru/public_v1/categories',
                    headers=headers)
            parse_attempts = 0
        except Exception as e:
            if parse_attempts == 0:
                raise e
            time.sleep(parse_timeout)
    _delay()

    categories_ids = _extract_categories_ids(response)

    return categories_ids


def _extract_categories_ids(response: requests.Response) -> list[int]:
    categories = [category for category in response.json()]
    result = []
    while categories:
        category = categories.pop(0)
        if category['__children']:
            for sub_category in category['__children']:
                categories.append(sub_category)
        else:
            result.append(category['id'])

    return result


def get_category_product_data(category_id: int) -> dict:
    """Fucntion requests to bonjure-dv API and 
    gets json with category product data."""

    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://bonjour-dv.ru',
        'Connection': 'keep-alive',
        'Referer': 'https://bonjour-dv.ru/',
        # 'Cookie': 'PHPSESSID=nibfu1qkst0hurul7jm4d8k9kf',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    params = {
        'filter[categories]': category_id,
        'offset': '0',
        'resourceId': category_id,
    }

    parse_attempts = config.PARSE_ATTEMPTES
    parse_timeout = config.PARSE_TIMEOUT
    while parse_attempts > 0:
        parse_attempts -= 1
        try:
            response = requests.get('https://api.bonjour-dv.ru/public_v1/products', params=params, headers=headers)
            parse_attempts = 0
        except Exception as e:
            if parse_attempts == 0:
                raise e
            time.sleep(parse_timeout)
    _delay()

    return response.json()


def main() -> None:
    pass


if __name__ == "__main__":
    main()

