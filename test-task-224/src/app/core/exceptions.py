from typing import Mapping

from src.config import settings


class ApiException(Exception):
    """
    Base class for API exceptions
    """

    status_code: int = 500
    message: str = "Упс! Что-то пошло не так ;("

    def __init__(self, message: str | None = None, payload: Mapping | None = None, exception_class: str | None = None):
        self.message = message or self.message
        self.payload = payload
        self.exception_class = exception_class

    def _type(self):
        return self.__class__.__name__

    def to_json(self) -> Mapping:
        return {"code": self.status_code, "message": self.message, "payload": self.payload}


class ServerError(ApiException):
    status_code = 500
    message = "Упс! Что-то пошло не так ;("


class NotFoundError(ApiException):
    status_code = 404
    message = "Not Found"


class ObjectNotFoundError(ApiException):
    status_code = 404
    message = "Not Found"


class BadRequestError(ApiException):
    status_code = 400
    message = "Bad Request"


class ObsceneLanguageError(ApiException):
    status_code = 400
    message = "Obscene language found"


class EmailTakenError(ApiException):
    status_code = 400
    message = "Email already taken"


class ValidationError(ApiException):
    message = "Validation Error"
    status_code = 400


class UserNotFoundError(ApiException):
    status_code = 400
    message = "User not found"


class PasswordMatchError(ApiException):
    status_code = 400
    message = "Password doesn't match"


class UnsupportedFileTypeError(ApiException):
    status_code = 400
    message = f"Provide only: {settings.ALLOWED_UPLOAD_TYPES}"


class FileTooLargeError(ApiException):
    status_code = 400
    message = f"Max file size: {settings.FILE_MAX_SIZE_MB} Mb"


class NeedEmailConfirmation(ApiException):
    status_code = 400
    message = "You need to confirm email"


class UnauthorizedError(ApiException):
    status_code = 401
    message = "Unauthorized"


class ForbiddenError(ApiException):
    status_code = 403
    message = "Forbidden"


class JWTExpiredSignatureError(ApiException):
    status_code = 426
    message = "Token expired"


class JWTDecodeError(ApiException):
    status_code = 401
    message = "Token decode error"


class ItemNotFoundError(NotFoundError):  # there might be constructor as {x} not found
    message = "Item not found"


class CharacterNotFoundError(NotFoundError):
    message = "Character not found"
