# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://lk.megafon.ru/login/')
    check_status_code(response, 200)

    csrf_token = re.search(r'name="CSRF" value="(.*?)"', response.content)

    if csrf_token is None:
        raise BadResponse('CSRF token not found', response)

    csrf_token = csrf_token.group(1)

    response = s.post('https://lk.megafon.ru/dologin/',
                      data={'j_username': number,
                            'j_password': password,
                            'CSRF': csrf_token,
                        })
    check_status_code(response, 200)

    if u'Требуется ввод цифрового кода' in response.text:
        raise BadResponse('CAPTCHA was shown', response)
    if u'Как получить пароль' in response.text:
        raise BadResponse('Bad password or login', response)

    response = s.get('https://lk.megafon.ru/api/lk/balance/get')

    check_status_code(response, 200)

    data = response.json()
    return data['balance']
