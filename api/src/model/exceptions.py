from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND


class DetailedHTTPException(HTTPException):
    STATUS_CODE = HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = 'Server error'

    def __init__(self):
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = HTTP_401_UNAUTHORIZED
    DETAIL = 'User not authenticated'


class BadRequest(DetailedHTTPException):
    STATUS_CODE = HTTP_400_BAD_REQUEST
    DETAIL = 'Bad request'


class AlreadyRegistered(DetailedHTTPException):
    STATUS_CODE = HTTP_400_BAD_REQUEST
    DETAIL = 'Username already registered'


class NotFound(DetailedHTTPException):
    STATUS_CODE = HTTP_404_NOT_FOUND
