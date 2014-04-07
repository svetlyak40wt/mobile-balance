import requests
import re


def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://my.tele2.ru/public/login')
    csrf_field, csrf_value = re.search(r'name="csrfTok(.*?)" value="(.*?)"', response.content).groups()
    csrf_field = 'csrfTok%s' % csrf_field

    response = s.post('https://my.tele2.ru/public/security/check',
        data={csrf_field: csrf_value, 'j_username': number, 'j_password': password})
    csrf_field, csrf_value = re.search(r"csrfTok(.*?): '(.*?)'", response.content).groups()
    csrf_field = 'csrfTok%s' % csrf_field

    response = s.post('https://my.tele2.ru/balance/json',
        data={csrf_field: csrf_value, 'isBalanceRefresh': 'true'})

    return float(response.json()['balance'].split()[0].replace(',', '.'))
