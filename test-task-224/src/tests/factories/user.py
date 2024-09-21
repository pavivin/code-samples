import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from faker import Factory as FakerFactory
from pwdlib import PasswordHash
from pytest_factoryboy import register

from src.app.auth.models import User
from src.db.base import sc_session

faker = FakerFactory.create()


def get_password_hash(password: str):  # hardcode string result
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)


@register
class UserFactory(AsyncSQLAlchemyFactory):
    # first_name = factory.LazyAttribute(lambda x: faker.name())
    # last_name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    hashed_password = factory.LazyAttribute(lambda x: get_password_hash("string"))

    class Meta:
        model = User
        sqlalchemy_session = sc_session
