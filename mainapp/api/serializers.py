from mainapp import models
from mainapp.logic.balance import get_balance
from .helpers import SerializerWriteAllowMethodField
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(
        source='get_balance', read_only=True
        )
    username = SerializerWriteAllowMethodField(
        source='get_username'
        )

    class Meta:
        model=models.Account
        fields=('uid', 'created', 'updated', 'balance', 'username')

    def get_balance(self, obj: models.Account):
        balance = get_balance(obj)
        return balance
    
    def get_username(self, obj: models.Account):
        return obj.user.username
    
    def update(self, instance: models.Account, validated_data: dict):
        username = validated_data.get('username')
        if username is not None:
            instance.user.username = username
            instance.user.save(update_fields=['username'])
        return super().update(instance, validated_data)
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ('pk', 'username', 'password')
        write_only_fields = ('password',)
        
    def create(self, validated_data):
        user = models.Users.objects.create_user(**validated_data)
        return user
