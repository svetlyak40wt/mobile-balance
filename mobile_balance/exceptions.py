class BadResponse(Exception):
    def __init__(self, message, response):
        super(BadResponse, self).__init__(message)
        self.response = response
