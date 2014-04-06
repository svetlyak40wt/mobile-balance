#!/usr/bin/env python

import requests
import re
import anyjson



def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://login.mts.ru/amserver/UI/Login')
    csrf_sign = re.search(r'name="csrf.sign" value="(.*?)"', response.content).group(1)

    response = s.post('https://login.mts.ru/amserver/UI/Login?service=lk&goto=https://lk.ssl.mts.ru/',
                      data={'IDToken1': number,
                            'IDToken2': password,
                            'csrf.sign': csrf_sign,
                        },
                      headers={
                          'Accept-Language': 'ru,en;q=0.8',
                      })

    data = anyjson.deserialize(s.get('https://lk.ssl.mts.ru/ProfileStub/PAGet').content)
    return data.get('Balance')
