from unittest import TestCase
from users_service.tests.roman_numerals import from_roman_to_arabic
import pytest

from fastapi.testclient import TestClient
from main import app
from queries.users import UserIn, UserRepository

client = TestClient(app)

class EmptyUserRepository:
    def create_users(self):
        return []



def create_test(self, User):
    result = {}
    #Arrange

    #Act

    #Assert


