#!/usr/bin/env python

"""MTS Balance.

Usage:
  mts.py --number=<phone-number> --password=<password>
  mts.py (-h | --help)
  mts.py --version

Options:
  -h --help                Show this screen.
  --version                Show version.
  --number=<phone-number>  Mobile number without 8 or +7 prefix.
  --password=<password>    Password from personal profile at https://lk.ssl.mts.ru/

"""

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


if __name__ == '__main__':
    arguments = docopt(__doc__, version='MTS Balance 0.1.0')
    print get_balance(arguments['--number'],
                      arguments['--password'])
