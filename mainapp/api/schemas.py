from typing import Optional, Type
from pydantic import BaseModel, ValidationError
from .exceptions import APIValidationError


class RequestSchema(BaseModel):
    pass 


class ResponseSchema(BaseModel):
    pass


class DepositWithdrawSchema(RequestSchema):
    delta: int
    
    
class TransferSchema(RequestSchema):
    delta: int
    uid: str
    

class DepositWithdrawResponseSchema(ResponseSchema):
    sum: int

    
def validate_input(schema: Type[RequestSchema], data: dict) -> Optional[BaseModel]:
    try:
        validated_data = schema(**data)
    except ValidationError as e:
        print(e.errors())
        raise APIValidationError(e.errors())
    return validated_data
    