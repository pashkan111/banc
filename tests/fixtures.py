import pytest
from mainapp.models import Users, Account


@pytest.fixture
@pytest.mark.django_db
def create_accounts():
    user1 = Users.objects.create_user(
        username='pashkan', password='1234qwer'
        )
    user2 = Users.objects.create_user(
        username='ivan', password='1234asdf'
        )
    account1 = Account.objects.create(user=user1)
    account2 = Account.objects.create(user=user2)
