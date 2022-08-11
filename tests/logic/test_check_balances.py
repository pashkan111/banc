from mainapp.logic.balance import check_balances
from tests.fixtures import accounts,  deposit
import pytest
from exceptions.balance_exceptions import LimitExceeded, NotEnoughMoney


@pytest.mark.django_db
def test_check_balances(accounts, deposit):
    """
    Тестирует функцию проверки баланса аккаунтов
    """
    account1 = accounts[0]
    account2 = accounts[1]
    # Тестирует случай, когда счет пополняют на сумму, превышающую лимит
    with pytest.raises(LimitExceeded) as exc:
        check_balances(
            delta=1000000,
            account_deposit_uid=account1.uid
            )
        assert 'Limit exceeded' in str(exc.value)
        
    with pytest.raises(NotEnoughMoney) as exc:
        check_balances(
            delta=10000,
            account_deposit_uid=account1.uid,
            account_withdraw_uid=account2.uid
            )
        assert 'Not enough money on balance' in str(exc.value)
