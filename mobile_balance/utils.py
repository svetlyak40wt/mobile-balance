import re

from .exceptions import BadResponse


def check_status_code(response, expected_code):
    result_code = response.status_code

    if result_code != expected_code:
        url = response.url
        method = response.request.method

        raise BadResponse(('{method} to {url} resulted '
                           'in {result_code} status code '
                           'instead of {expected_code}').format(
            **locals()),
            response)


def cleanup_phone_number(number):
    number_clean = re.sub(r'\D', '', number)
    if len(number_clean) == 11 and number_clean[0] != '7':
        number_clean = '7{}' + number_clean[1:]
    elif len(number_clean) == 10:
        number_clean = '7{}' + number_clean
    if not re.match(r'^7\d{10}$', number_clean):
        raise ValueError('Incorrect phone number format. Must be 7XXXXXXXXXX')
    return number_clean
