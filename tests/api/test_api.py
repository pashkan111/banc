from tests.fixtures import accounts, api_client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from mainapp.models import Users, Account, Action
import pytest


def setup():
    print ("basic setup into module===================")
    
def setup_module(module):
    print ("module setup000000000000000")
    

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
        account=account, delta=test_sum
    )
    assert response.status_code == 201
    assert action.count() == 1


# @pytest.mark.django_db
# def test_WithdrawMoneyView(accounts, api_client):
#     """
#     Тестирует апи для снятия денег.
#     Рассматриваются 2 варианта: когда денег на счету достаточно
#     и когда нет
#     """
#     test_sum = 1500
#     url = reverse('deposit')
#     body = {
#         "delta": test_sum
#     }
#     account: Account = accounts[0]
#     # Пополняем ба
#     Action.objects.create(
#         balance_action=Action.BalanceAction.DEPOSITED,
#         payment_type=Action.PaymentType.CASH,
#         account=account,
#         delta=2000
#     )
    
#     token = Token.objects.create(user=account.user)
#     api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
#     response = api_client.post(url, body)
#     action = Action.objects.filter(
#         account=account, delta=test_sum
#     )
#     assert response.status_code == 201
#     assert action.count() == 1