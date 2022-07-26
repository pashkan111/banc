from exceptions.balance_exceptions import InvalidSum, LimitExceeded
from typing import Optional


def validate_money(sum: int) -> Optional[int]:
    if not type(sum) == int:
        raise ValueError
    if sum <= 0:
        raise InvalidSum
    # if (self.balance + sum) > self.MAX_BALANCE:
    #     raise LimitExceeded
    return sum