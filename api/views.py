from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransferSerializer
from django.contrib import messages
from base.models import Ledger, User, Transfer, BankAccount, Profile
from base.utils import get_transfer

# Create your views here.


def getRouter(request):
    data = {
        "content": "Welcome to Fin API"
    }
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def transfer(request):
    if request.method == 'POST':
        account_id = request.data['accountid']
        amount = request.data['amount']

        receiver_account = BankAccount.objects.get(account_id=account_id).user

        transfer = Transfer.objects.create(
            receiver=receiver_account,
            amount=amount,
        )

        transaction = Transaction.objects.create(
            transfer=transfer
        )

        Ledger.objects.create(
            sender=request.user.username,
            receiver=receiver_account,
            amount=amount,
            transaction_id=transaction.tran_id
        )

    transfers = Transfer.objects.all()
    serializer = TransferSerializer(transfers, many=True)
    return Response(serializer.data)
