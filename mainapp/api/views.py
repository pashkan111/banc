from rest_framework import views, response, status, viewsets
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated, AllowAny
from mainapp.models import Action, Users, Account
from .serializers import (
    UserSerializer, AccountSerializer, ActionSerializer
    )
from .schemas import (
    DepositWithdrawSchema, validate_input, TransferSchema, 
    DepositWithdrawResponseSchema
    )
from mainapp.logic.action import ActionCreator
from mainapp.logic.balance import check_balances, AccountBalance


class DepositMoneyView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: HttpRequest):
        user: Users = request.user
        account: Account = user.account
        validated_data = validate_input(DepositWithdrawSchema, request.data)
        check_balances(
            delta=validated_data.delta,
            account_deposit_uid= account.uid
            )
        ActionCreator(account=account, delta=validated_data.delta).deposit()
        balance = AccountBalance.get_balance(account)
        resp = DepositWithdrawResponseSchema(sum=balance)
        return response.Response(data=resp.dict(), status=status.HTTP_201_CREATED)


class WithdrawMoneyView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: HttpRequest):
        user: Users = request.user
        account: Account = user.account
        validated_data = validate_input(DepositWithdrawSchema, request.data)
        check_balances(
            delta=validated_data.delta,
            account_withdraw_uid=account.uid
            )
        ActionCreator(account=account, delta=validated_data.delta).withdraw_money()
        balance = AccountBalance.get_balance(account)
        resp = DepositWithdrawResponseSchema(sum=balance)
        return response.Response(data=resp.dict(), status=status.HTTP_200_OK)
    
    
class TransferMoneyView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: HttpRequest):
        user: Users = request.user
        account_from: Account = user.account
        validated_data = validate_input(TransferSchema, request.data)
        account_to = Account.get_account_by_id(validated_data.uid)
        check_balances(
            delta=validated_data.delta,
            account_deposit_uid=account_to.uid,
            account_withdraw_uid=account_from.uid,
            )
        ActionCreator(
            account=account_to,
            account_from=account_from,
            delta=validated_data.delta
            ).transfer_money()
        balance = AccountBalance.get_balance(account_from)
        resp = DepositWithdrawResponseSchema(sum=balance)
        return response.Response(data=resp.dict(), status=status.HTTP_201_CREATED)


class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        account = user.account
        return account
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        
        
class ActionView(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user: Users = self.request.user
        account: Account = user.account
        return Action.objects.filter(account=account)
        

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
