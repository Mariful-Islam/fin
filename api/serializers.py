from rest_framework.serializers import ModelSerializer
from base.models import *


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
