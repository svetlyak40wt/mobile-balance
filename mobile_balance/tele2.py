# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    s = requests.Session()

    response = s.post('https://login.tele2.ru:443/ssotele2/wap/auth/submitLoginAndPassword',
                      data={'pNumber': number, 'password': password})
    check_status_code(response, 200)

    response = s.get('https://my.tele2.ru/home')
    check_status_code(response, 200)

    match = re.search(r"csrfTok(.*?): '(.*?)'", response.content)
    if match is None:
        raise BadResponse('CSRF token not found', response)

    csrf_field, csrf_value = match.groups()
    csrf_field = 'csrfTok%s' % csrf_field

    response = s.post('https://my.tele2.ru/balance/json',
                      data={csrf_field: csrf_value, 'isBalanceRefresh': 'true'})
    check_status_code(response, 200)

    balance = response.json().get('balance')
    if balance is None:
        raise BadResponse('Unable to get balance from JSON', response)

    return float(balance.split()[0].replace(',', '.'))
