from tests.fixtures import accounts, api_client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from mainapp.models import Users, Account, Action
import pytest


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
