# coding: utf-8

import requests
import re
import time

from .exceptions import BadResponse
from .utils import check_status_code

from bs4 import BeautifulSoup

def get_balance(number, password):
    s = requests.Session()

    # https://szf.b2blk.megafon.ru currently has an issue with its certificates chain
    response = s.get('https://szf.b2blk.megafon.ru/b2b/login', verify=False)

    check_status_code(response, 200)

    millis = int(round(time.time() * 1000))

    response = s.post('https://szf.b2blk.megafon.ru/b2b/loginProcess',
                      data={'username': number,
                            'password': password,
                            'captchaTime': millis,
                        })
    check_status_code(response, 200)

    soup = BeautifulSoup(response.text)
    data = soup.findAll('span', {'class': 'money bold'})
    return data[0].get_text()
