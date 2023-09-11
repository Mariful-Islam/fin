from rest_framework.serializers import ModelSerializer
from base.models import User, Transaction, Transfer, BankAccount, Message, Profile


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
