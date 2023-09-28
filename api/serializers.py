from rest_framework.serializers import ModelSerializer
from base.models import *
from django.contrib.auth.models import AbstractUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"


class LedgerSerializer(ModelSerializer):
    class Meta:
        model = Ledger
        fields = "__all__"


class BankAccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id",
                  "account_id",
                  "balance", "get_username"]


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id",
                  "address",
                  "bio",
                  "user",
                  "get_username",
                  "get_name",
                  "get_email",
                  "get_avater"]


class RevenueSerializer(ModelSerializer):
    class Meta:
        model = Revenue
        fields = "__all__"


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'avater', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            avater=validated_data['avater'],
            password=validated_data['password']
        )
        return user


# User serializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
