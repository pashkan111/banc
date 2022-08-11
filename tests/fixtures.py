import pytest
from mainapp.models import Users, Account, Action
from rest_framework.test import APIClient
from typing import List
from rest_framework.authtoken.models import Token


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
    return [account1, account2]


@pytest.fixture
@pytest.mark.django_db
def deposit(accounts: List[Account]):
    """
    Пополняем баланс тестовых аккаунтов
    """
    account1 = accounts[0]
    account2 = accounts[1]
    Action.objects.create(
        balance_action=Action.BalanceAction.DEPOSITED,
        payment_type=Action.PaymentType.CASH,
        account=account1,
        delta=2000
    )
    Action.objects.create(
        balance_action=Action.BalanceAction.DEPOSITED,
        payment_type=Action.PaymentType.CASH,
        account=account2,
        delta=1500
    )


@pytest.fixture
def api_client():
    client = APIClient()
    return client

