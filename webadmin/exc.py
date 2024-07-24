from fastapi import HTTPException

class NotAuthenticatedException(HTTPException):
    pass

class NotAccessException(HTTPException):
    pass

class NewsletterException(HTTPException):
    pass



class UpdateQuestionException(HTTPException):
    pass