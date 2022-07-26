from mainapp.models import Account, Action
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce


def get_balance(account: Account) -> int:
    "Return balance of the account"
    balance = Action.objects.filter(account=account)\
    .annotate(
        deposited=Coalesce(Sum('delta', filter=Q(balance_action=Action.BalanceAction.DEPOSITED)), 0), 
        withdrawned=Coalesce(Sum('delta', filter=Q(balance_action=Action.BalanceAction.WITHDRAWNED)), 0)
    )\
    .aggregate(sum=Sum(F('deposited') - F('withdrawned')))
    return balance['sum']
