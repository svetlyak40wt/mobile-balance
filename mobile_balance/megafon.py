import requests
import re
import anyjson


def get_balance(number, password):
    s = requests.Session()

    response = s.get('https://lk.megafon.ru/login/')
    csrf_token = re.search(r'name=CSRF value="(.*?)"', response.content).group(1)

    response = s.post('https://lk.megafon.ru/dologin/',
                      data={'j_username': number,
                            'j_password': password,
                            'CSRF': csrf_token,
                        })

    content = s.get('https://lk.megafon.ru/').content
    match = re.search(r'<div class="[^"]*ui-label-balance".*?([\d,]+).*?</div>',
                      content)
    return match.group(1).replace(',', '.')
