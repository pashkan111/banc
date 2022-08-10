from django.urls import path
from . import views


urlpatterns = [
    path('deposit', views.DepositMoneyView.as_view(), name='deposit'),
    path('transfer', views.TransferMoneyView.as_view()),
    path('withdraw', views.WithdrawMoneyView.as_view(), name='withdraw'),
    path('users', views.UserView.as_view({'post': 'create'})),
    path('account', views.AccountView.as_view({
        'get': 'retrieve', 'patch': 'update'
        })),
    path('history', views.ActionView.as_view({'get': 'list'})),
]
