from fastapi import HTTPException

class NotAuthenticatedException(HTTPException):
    pass


class NewsletterException(HTTPException):
    pass