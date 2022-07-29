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


def check_balances(
    delta: int,
    account_deposit_uid: Optional[Account]=None, 
    account_withdraw_uid: Optional[Account]=None, 
    ) -> Optional[bool]:
    """Checks limits of accounts"""
    if not any((account_deposit_uid, account_withdraw_uid)):
        raise Exception
    with atomic():
        if account_deposit_uid is not None:
            account_deposit = Account.objects.filter(
                uid=account_deposit_uid
                ).select_for_update(nowait=True).get()
            account_balance = AccountBalance.get_balance(account_deposit)
            account_balance += delta
            if account_balance > Account.MAX_BALANCE:
                raise LimitExceeded
        if account_withdraw_uid is not None:
            account_withdraw = Account.objects.filter(
                uid=account_withdraw_uid
                ).select_for_update(nowait=True).get()
            account_from_balance = AccountBalance.get_balance(account_withdraw)
            account_from_balance -= delta
            if account_from_balance < Account.MIN_BALANCE:
                raise NotEnoughMoney
        return True
    
    