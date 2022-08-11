from rest_framework.exceptions import NotFound


class AccountNotFound(NotFound):
    default_detail = ('Account not found')