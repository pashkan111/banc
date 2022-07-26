from mainapp.models import Action, Account
from typing import Optional


class Error(Exception):
    pass


class ActionCreator:
    def __init__(
        self,
        account: Account,
        delta: int,
        payment_type: Optional[Action.PaymentType]=Action.PaymentType.NONE,
        comment: Optional[str]=None,
        account_from: Optional[Account]=None,
        balance_action: Optional[Action.BalanceAction]=Action.BalanceAction.DEPOSITED,
        ):
        self.account = account
        self.balance_action = balance_action
        self.payment_type = payment_type
        self.delta = delta
        self.comment = comment
        self.account_from = account_from
        
    def create_account(self):
        """Starts when client creating account"""
        Action.objects.create(
            account=self.account,
            balance_action=self.balance_action.CREATED
        )
        
    def deposit(self):
        """Starts when client makes a deposit"""
        Action.objects.create(
            account=self.account,
            balance_action=self.balance_action.DEPOSITED,
            delta=self.delta,
            payment_type=self.payment_type.CASH            
        )
    
    def transfer_money(self):
        """Transfer money to client"""
        Action.objects.create(
            account=self.account,
            account_from=self.account_from,
            balance_action=self.balance_action.DEPOSITED,
            delta=self.delta,
            payment_type=self.payment_type.TRANSFER            
        )
        Action.objects.create(
            account=self.account_from,
            balance_action=self.balance_action.WITHDRAWNED,
            delta=self.delta,
            payment_type=self.payment_type.TRANSFER            
        )
    
    def takeout_money(self):
        """Take out money from account"""
        Action.objects.create(
            account=self.account,
            balance_action=self.balance_action.WITHDRAWNED,
            delta=self.delta,
            payment_type=self.payment_type.CASH            
        )

        