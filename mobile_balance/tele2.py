# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://login.tele2.ru/ssotele2/wap/auth/')
    check_status_code(response, 200)

    match = re.search(r'value="(.*?)" name="_csrf"', response.content)
    csrf_token = match.group(1)
    if csrf_token is None:
        raise BadResponse('CSRF token not found', response)

    data = dict(pNumber=number, password=password, _csrf=csrf_token)
    response = s.post(
        'https://login.tele2.ru/ssotele2/wap/auth/submitLoginAndPassword',
        data=data)
    check_status_code(response, 200)

    response = s.get('https://my.tele2.ru/main/tariffAndBalance')
    check_status_code(response, 200)

    balance = response.json().get('balance')
    if balance is not None:
        amount = balance.get('amount')
    if balance is None or amount is None:
        raise BadResponse('Unable to get balance amount from JSON', response)

    return float(amount.split()[0].replace(',', '.'))
