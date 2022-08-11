from exceptions.balance_exceptions import InvalidSum
from typing import Optional


def validate_money(sum: int) -> Optional[int]:
    if not type(sum) == int:
        raise ValueError
    if sum <= 0:
        raise InvalidSum
    return sum