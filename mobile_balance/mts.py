#!/usr/bin/env python

import requests
import re


def get_balance(number, password):
    session = requests.Session()

    response = session.get('https://login.mts.ru/amserver/UI/Login')
    csrf_token = re.search(r'name="csrf.sign" value="(.*?)"', response.content).group(1)

    response = session.post('https://login.mts.ru/amserver/UI/Login?service=lk&goto=https://lk.ssl.mts.ru/',
                      data={'IDToken1': number,
                            'IDToken2': password,
                            'csrf.sign': csrf_token,
                        },
                      headers={
                          'Accept-Language': 'ru,en;q=0.8',
                      })
    assert response.status_code == 200

    response = session.get('https://lk.ssl.mts.ru/ProfileStub/PAGet')
    assert response.status_code == 200

    data = response.json()
    balance = data.get('Balance')
    if balance:
        return float(balance)
