# coding: utf-8

import requests
import re

from .exceptions import BadResponse
from .utils import check_status_code


def get_balance(number, password):
    params = {'class': 'CStatWS', 'op': 'GetBalance', 'directcall': 1}
    response = requests.get('https://%s:%s@stat.myttk.ru/soap/'
                            % (number, password), params=params)
    check_status_code(response, 200)

    match = re.search(r"<result>(.*?)</result>", response.content)
    balance = match.group(1)

    if balance is None:
        raise BadResponse('Unable to get balance from XML', response)

    return float(balance)
