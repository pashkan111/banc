import pytest
from mainapp.models import Account, Users


@pytest.fixture
def create_account():
    account = Account.objects.create()