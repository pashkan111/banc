from django.contrib import admin
from .models import Account, Action, Aggregates


admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Aggregates)