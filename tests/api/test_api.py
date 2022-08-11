from tests.fixtures import accounts, api_client, deposit
from django.urls import reverse
from rest_framework.authtoken.models import Token
from mainapp.models import Account, Action
import pytest
from exceptions.balance_exceptions import LimitExceeded, NotEnoughMoney
from exceptions.account_exceptions import AccountNotFound
import uuid


@pytest.mark.django_db
def test_DepositMoneyView(accounts, api_client):
    """
    Тестирует апи для внесения депозита
    """
    test_sum = 1500
    url = reverse('deposit')
    body = {
        "delta": test_sum
    }
    account: Account = accounts[0]
    token = Token.objects.create(user=account.user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = api_client.post(url, body)
    action = Action.objects.filter(
        account=account, 
        delta=test_sum,
        balance_action=Action.BalanceAction.DEPOSITED
    )
    assert response.status_code == 201
    assert action.count() == 1


@pytest.mark.django_db
def test_WithdrawMoneyView(deposit, api_client, accounts):
    """
    Тестирует апи для снятия денег.
    Рассматриваются 2 варианта: когда денег на счету достаточно
    и когда нет
    """
    test_sum = 1700
    url = reverse('withdraw')
    body = {
        "delta": test_sum
    }
    account: Account = accounts[0]
    
    token = Token.objects.create(user=account.user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = api_client.post(url, body)
    action = Action.objects.filter(
        account=account,
        delta=test_sum, 
        balance_action=Action.BalanceAction.WITHDRAWNED
    )
    assert response.status_code == 200
    assert action.count() == 1
    
    response = api_client.post(url, body)
    assert response.status_code == 400


class TestTransferMoneyView:
    """
        Тестирует апи для перевода денег.
        Рассматриваются 4 варианта: 
        1. Когда все ок
        2. Когда на балансе недостаточно денег
        3. Когда общий баланс после перевода превышает лимит
        4. Когда аккаунт не найден
    """
    url = reverse('transfer')

    @pytest.mark.django_db
    def test_ok(self, deposit, api_client, accounts):
        account1: Account = accounts[0]
        account2: Account = accounts[1]
        test_sum = 1700
        body = {
            "delta": test_sum,
            "uid": account2.uid
        }
        
        token = Token.objects.create(user=account1.user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(self.url, body)
        action1 = Action.objects.filter(
            account=account1,
            delta=test_sum, 
            balance_action=Action.BalanceAction.WITHDRAWNED
        )
        action2 = Action.objects.filter(
            account=account2,
            delta=test_sum, 
            balance_action=Action.BalanceAction.DEPOSITED
        )
        assert response.status_code == 201
        assert action1.count() == 1
        assert action2.count() == 1

    @pytest.mark.django_db
    def test_acc_has_not_enough_money(self, deposit, api_client, accounts):
        account1: Account = accounts[0]
        account2: Account = accounts[1]
        test_sum = 2700
        body = {
            "delta": test_sum,
            "uid": account2.uid
        }
        token = Token.objects.create(user=account1.user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(self.url, body)
        assert response.status_code == 400  
        assert response.data['detail'] == NotEnoughMoney.default_detail

    @pytest.mark.django_db
    def test_acc_has_limit_exceed(self, deposit, api_client, accounts):
        account1: Account = accounts[0]
        account2: Account = accounts[1]
        test_sum = 1000000
        body = {
            "delta": test_sum,
            "uid": account2.uid
        }
        token = Token.objects.create(user=account1.user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(self.url, body)
        assert response.status_code == 400
        assert response.data['detail'] == LimitExceeded.default_detail
        
    @pytest.mark.django_db
    def test_acc_has_not_found(self, deposit, api_client, accounts):
        account1: Account = accounts[0]
        test_sum = 1000
        body = {
            "delta": test_sum,
            "uid": uuid.uuid4().hex
        }
        token = Token.objects.create(user=account1.user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(self.url, body)
        assert response.status_code == 404
        assert response.data['detail'] == AccountNotFound.default_detail