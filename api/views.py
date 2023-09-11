from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransactionSerializer, TransferSerializer
from django.contrib import messages
from base.models import User, Transfer, Transaction, BankAccount, Profile


# Create your views here.


def getRouter(request):
    data = {
        "content": "Welcome to Fin API"
    }
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def transfer(request):

    if request.method == "POST":
        account_id = request.data['account_id']
        amount = request.data['amount']
        try:
            receiver_account = BankAccount.objects.get(account_id=account_id)
            receiver = receiver_account.user

            transfer = Transfer.objects.create(
                receiver=receiver,
                amount=amount
            )
            transaction = Transaction.objects.create(transfer=transfer)

            transfer.save()
            transaction.save()

            # balance system
            sender_account = BankAccount.objects.get(user=request.user)
            sender_balance = sender_account.balance

            receiver_balance = receiver_account.balance

            sender_balance = sender_balance-transfer.amount
            receiver_balance = receiver_balance+transfer.amount

            sender_account.objects.update(balance=sender_balance)
            receiver_account.objects.update(balance=receiver_balance)

            messages.info(
                request, 'You successfully sent {}$ to {}.'.format(amount, receiver))

        except:
            messages.info(request, 'No User Found')
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)

    return Response(serializer.data)
