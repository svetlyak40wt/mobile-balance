# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code, cleanup_phone_number


def get_balance(number, password):
    s = requests.Session()
    # API expects phone number in strict international format
    # Only digits: <COUNTRY_CODE><ABC/DEF><PHONE_NUMBER>
    number = cleanup_phone_number(number)

    data = {"client_id": "digital-suite-web-app",
            "grant_type": "password",
            "username": number,
            "password": password,
            "password_type": "password",
            }
    response = s.post('https://my.tele2.ru/auth/realms/tele2-b2c/protocol/openid-connect/token', data=data)

    if not response.ok:
        print(response, response.content)
        raise ValueError('Authentication Failed')

    token = response.json()['access_token']
    s.headers.update({'Authorization': 'Bearer {}'.format(token)})

    response = s.get('https://my.tele2.ru/api/subscribers/{}/balance'.format(number))
    check_status_code(response, 200)

    amount = response.json().get('data', {}).get('value', None)
    if amount is None:
        raise BadResponse('Unable to get balance amount from JSON', response)

    return amount
