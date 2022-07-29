from django.urls import path
from . import views


urlpatterns = [
    path('deposit', views.DepositMoneyView.as_view()),
    path('transfer', views.TransferMoneyView.as_view()),
    path('users', views.UserView.as_view({'post': 'create'})),
    path('account', views.AccountView.as_view({
        'get': 'retrieve', 'patch': 'update'
        })),
]
