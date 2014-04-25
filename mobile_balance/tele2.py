# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://my.tele2.ru/public/login')
    check_status_code(response, 200)

    match = re.search(r'name="csrfTok(.*?)" value="(.*?)"', response.content)
    if match is None:
        raise BadResponse('CSRF token not found', response)
        
    csrf_field, csrf_value = match.groups()
    csrf_field = 'csrfTok%s' % csrf_field

    response = s.post('https://my.tele2.ru/public/security/check',
        data={csrf_field: csrf_value, 'j_username': number, 'j_password': password})
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
