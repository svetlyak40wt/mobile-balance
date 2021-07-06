# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    s = requests.Session()
    try:
        response = s.get('https://lk.megafon.ru/login/')
        check_status_code(response, 200)
    except:
        print('Unable to get the data from Megafon site. Exiting!')
        exit(1)
    
        # Replaced the cookie search
    try:
        csrf_token = response.cookies['CSRF-TOKEN']
    except:
        print('Unable to get the Megafon auth token. Exiting!')
        exit(1)


    if csrf_token is None:
        raise BadResponse('CSRF token not found', response)
    try:
        response = s.post('https://lk.megafon.ru/dologin/',
                        data={'j_username': number,
                                'j_password': password,
                                'CSRF': csrf_token,
                            })
        check_status_code(response, 200)
    except: 
        raise BadResponse('Unable to login the Megafon site. Exiting!', response)
    
    if u'Символы с картинки' in response.text:
        raise BadResponse('CAPTCHA was shown', response)
    if u'Требуется ввод цифрового кода' in response.text:
        raise BadResponse('CAPTCHA was shown', response)
    if u'Как получить пароль' in response.text:
        raise BadResponse('Bad password or login', response)
    
    try:
        response = s.get('https://lk.megafon.ru/api/lk/balance/get')

        check_status_code(response, 200)
    
    except: 
        raise BadResponse('Unable to get Megafon balance', response)
    data = response.json()

    if 'balance' not in data:
        raise BadResponse('Unable to get Megafon balance', response)
    return data['balance']

