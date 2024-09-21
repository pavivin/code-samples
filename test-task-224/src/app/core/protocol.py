from typing import Any, Generic, TypeVar
import uuid

import orjson
import phonenumbers
from pydantic import BaseModel as PydanticModel, validator
from pydantic import Field
from pydantic.generics import GenericModel as PydanticGenericModel
from pydantic.validators import strict_str_validator


DataT = TypeVar("DataT")


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class BaseModel(PydanticModel):
    @validator("*", pre=True)
    def convert_uuid_to_string(cls, v: Any) -> Any:
        if isinstance(v, uuid.UUID):
            return str(v)
        return v

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        # alias_generator = to_camel_case
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            uuid.UUID: lambda v: str(v),
        }


class Response(PydanticGenericModel, Generic[DataT]):
    """
    Базовый ответ на запрос
    """

    code: int = Field(200, description="Код ответа (http-like)")
    message: str | None = Field(description="Описание кода ответа")
    payload: DataT | None = Field(None, description="Тело ответа")
    exception_class: str | None = Field(None, description="Имя класса ошибки")

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PhoneNumber(str):
    """Phone Number Pydantic type, using google's phonenumbers"""

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        v = v.strip().replace(" ", "")

        try:
            parsed_number = phonenumbers.parse(v)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("invalid phone number format")

        return cls(phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164))
