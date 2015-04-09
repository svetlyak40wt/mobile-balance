#!/usr/bin/env python

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    session = requests.Session()

    response = session.get('https://login.mts.ru/amserver/UI/Login')
    check_status_code(response, 401)

    csrf_token = re.search(r'name="csrf.sign" value="(.*?)"', response.content)

    if csrf_token is None:
        raise BadResponse('CSRF token not found', response)

    csrf_token = csrf_token.group(1)

    response = session.post('https://login.mts.ru/amserver/UI/Login?service=lk&goto=https://lk.ssl.mts.ru/',
                      data={'IDToken1': number,
                            'IDToken2': password,
                            'csrf.sign': csrf_token,
                        },
                      headers={
                          'Accept-Language': 'ru,en;q=0.8',
                      })
    check_status_code(response, 200)

    response = session.get('https://oauth.mts.ru/webapi-1.4/customers/@me')

    check_status_code(response, 200)

    data = response.json()
    relations = data['genericRelations']
    targets = [rel['target'] for rel in relations]
    accounts = [target for target in targets if target['@c'] == '.Account']

    if not accounts:
        raise RuntimeError('Account not found in the data response')

    balance = accounts[0].get('balance')

    if balance is None:
        raise BadResponse('Unable to get balance from JSON', response)

    return float(balance)
