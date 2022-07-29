from rest_framework.exceptions import APIException
from rest_framework import status


class LimitExceeded(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Limit exceeded')


class InvalidSum(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Invalid sum of money')


class NotEnoughMoney(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Not enough money on balance')