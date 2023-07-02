from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code

class InvalidRequestException(BaseCustomException):
    def __init__(self, detail):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)

class UserNameAlreadyExistException(BaseCustomException):
    def __init__(self):
        super().__init__("Such username already exist", status.HTTP_400_BAD_REQUEST)