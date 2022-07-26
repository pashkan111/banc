from rest_framework import views, response, status, viewsets
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated, AllowAny
from mainapp.models import Users, Account
from .serializers import (
    UserSerializer, AccountSerializer
    )
from .schemas import (
    DepositSchema, validate_input, TransferSchema
    )
from mainapp.logic.action import ActionCreator


class DepositMoneyView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: HttpRequest):
        user: Users = request.user
        account: Account = user.account
        validated_data = validate_input(DepositSchema, request.data)
        ActionCreator(account=account, delta=validated_data.delta).deposit()
        return response.Response(status=status.HTTP_201_CREATED)
    
    
class TransferMoneyView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: HttpRequest):
        user: Users = request.user
        account_from: Account = user.account
        validated_data = validate_input(TransferSchema, request.data)
        account_to = Account.get_account_by_id(validated_data.uid)
        ActionCreator(
            account=account_to,
            account_from=account_from,
            delta=validated_data.delta
            ).transfer_money()
        return response.Response(status=status.HTTP_201_CREATED)


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


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)