import pytest
from mainapp.models import Users, Account
from rest_framework.test import APIClient
from typing import List


@pytest.fixture
@pytest.mark.django_db
def accounts() -> List[Account]:
    user1 = Users.objects.create_user(
        username='pashkan', password='1234qwer'
        )
    user2 = Users.objects.create_user(
        username='ivan', password='1234asdf'
        )
    account1 = Account.objects.create(user=user1)
    account2 = Account.objects.create(user=user2)
    return account1, account2


@pytest.fixture
def api_client():
    client = APIClient()
    return client
