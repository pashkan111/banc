from typing import Optional
from django.db import models
import uuid
from helpers.enum_field import EnumField, DbEnum
from django.contrib.auth.models import AbstractUser
from exceptions.account_exceptions import AccountNotFound


class Users(AbstractUser):
    pass


class Account(models.Model):
    MAX_BALANCE = 1000000
    MIN_BALANCE = 0
    
    user = models.OneToOneField(Users, on_delete=models.PROTECT)
    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(
        null=True,
        blank=True,
    )
    balance = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'Account of {self.user.username}, {self.uid}'
    
    @classmethod
    def get_account_by_id(cls, uid: str) -> Optional['Account']:
        account = cls.objects.filter(uid=uid).first()
        if account is None:
            raise AccountNotFound
        return account
        

class Action(models.Model):
    class BalanceAction(DbEnum):
        CREATED = 'Created'
        UPDATED = 'Updated'
        DEPOSITED = 'Deposited'
        WITHDRAWNED = 'Withdrawned'
        
    class PaymentType(DbEnum):
        CASH = 'Cash'
        TRANSFER = 'Transfer'
        NONE = 'None'
        
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='to_account'
        )
    account_from = models.ForeignKey(
        Account, on_delete=models.PROTECT, null=True, blank=True
        )
    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True
        )
    created = models.DateTimeField(auto_now_add=True)
    balance_action = EnumField(
        enum=BalanceAction, 
        default=BalanceAction.CREATED
        )
    payment_type = EnumField(
        enum=PaymentType, 
        default=PaymentType.NONE
        )
    delta = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'Account ID - {self.account.id}. '\
            f'Action - {self.balance_action}. Delta - {self.delta}'


class AggregateManager(models.Manager):
    def get_current(self, account: Account):
        return self.get_queryset().filter(
            account=account
        ).order_by('date').last()


class Aggregates(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.PositiveIntegerField()
    objects = AggregateManager()

    def __str__(self):
        return f'The aggregate of {self.account.user.username} from '\
            f'{str(self.date)}'