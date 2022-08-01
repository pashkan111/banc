from celery import shared_task
from mainapp.logic.balance import AccountBalance


@shared_task
def make_aggregates_task():
    AccountBalance.make_aggregates_for_all_accounts()
