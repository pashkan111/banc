from typing import Optional
from mainapp.models import Account, Action
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce
from exceptions.balance_exceptions import LimitExceeded, NotEnoughMoney
from django.db.transaction import atomic


class AccountBalance:
    @classmethod
    def get_balance(cls, account: Account) -> int:
        "Return balance of the account"
        balance = Action.objects.filter(account=account)\
        .annotate(
            deposited=Coalesce(Sum('delta', filter=Q(balance_action=Action.BalanceAction.DEPOSITED)), 0), 
            withdrawned=Coalesce(Sum('delta', filter=Q(balance_action=Action.BalanceAction.WITHDRAWNED)), 0)
        )\
        .aggregate(sum=Sum(F('deposited') - F('withdrawned')))
        return balance['sum']
    
    @classmethod
    def set_balance(cls, account: Account, balance: int):
        account.balance = balance
        account.save(update_fields=['balance'])


def check_balances(
    account_uid: Account, account_from_uid: Account, delta: int
    ) -> Optional[bool]:
    """Checks limits of accounts"""
    with atomic():
        account = Account.objects.filter(
            uid=account_uid
            ).select_for_update(nowait=True).get()
        account_balance = account.balance
        account_balance += delta
        account_from = Account.objects.filter(
            uid=account_from_uid
            ).select_for_update(nowait=True).get()
        account_from_balance = account_from.balance
        account_from_balance -= delta
        if account_balance > Account.MAX_BALANCE:
            raise LimitExceeded
        if account_from_balance < Account.MAX_BALANCE:
            raise NotEnoughMoney
        return True
    
    