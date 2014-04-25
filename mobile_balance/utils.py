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
