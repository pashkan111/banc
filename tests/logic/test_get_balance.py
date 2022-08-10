from mainapp.logic.balance import AccountBalance
from tests.fixtures import accounts,  deposit
from mainapp.models import Users, Account, Action
import pytest


@pytest.mark.django_db
def test_get_balance(accounts, deposit):
    """
    Тестирует функцию получения баланса
    """
    account = accounts[0]
    balance = AccountBalance.get_balance(account)
    assert balance == 2000
    Action.objects.create(
        account=account,
        delta=5000,
        balance_action=Action.BalanceAction.DEPOSITED
    )
    Action.objects.create(
        account=account,
        delta=3000,
        balance_action=Action.BalanceAction.WITHDRAWNED
    )
    balance = AccountBalance.get_balance(account)
    assert balance == 4000