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

    response = s.get('https://login.tele2.ru/ssotele2/wap/auth/')
    check_status_code(response, 200)

    match = re.search(r'value="(.*?)" name="_csrf"', response.content)
    csrf_token = match.group(1)
    if csrf_token is None:
        raise BadResponse('CSRF token not found', response)

    data = dict(pNumber=number, password=password, _csrf=csrf_token, authBy='BY_PASS', rememberMe='true')
    response = s.post(
        'https://login.tele2.ru/ssotele2/wap/auth/submitLoginAndPassword',
        data=data)
    check_status_code(response, 200)

    response = s.get('https://my.tele2.ru/api/subscribers/{}/balance'.format(number))
    check_status_code(response, 200)

    amount = response.json().get('data', {}).get('value', None)
    if amount is None:
        raise BadResponse('Unable to get balance amount from JSON', response)

    return amount
