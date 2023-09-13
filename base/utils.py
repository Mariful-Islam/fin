from django.contrib import messages
from django.shortcuts import redirect
from base.models import *


def get_transfer(request):
    if request.method == "POST":
        account_id = request.POST['accountid']
        amount = request.POST['amount']
        try:
            receiver_account = BankAccount.objects.get(
                account_id=account_id)
            receiver = receiver_account.user
            sender_account = BankAccount.objects.get(user=request.user)

            transfer = Transfer.objects.create(
                receiver=receiver, amount=amount)
            transaction = Transaction.objects.create(transfer=transfer)

            transfer.save()
            transaction.save()

            ledger = Ledger.objects.create(sender=sender_account.user.username,
                                           receiver=receiver_account.user.username,
                                           amount=amount,
                                           transaction_id=transaction.tran_id)

            ledger.save()

            # balance system
            try:
                sender_account.balance = sender_account.balance-float(amount)
                receiver_account.balance = receiver_account.balance + \
                    float(amount)

                sender_account.save()
                receiver_account.save()

                messages.info(
                    request, 'You successfully sent {}$ to {}.'.format(amount, receiver))
            except:
                messages.info(request, 'Balance not updated')

        except:
            messages.info(request, 'No User Found')
        return redirect('transfer')


def get_transaction(request):
    try:
        transactions = Ledger.objects.filter(
            sender=request.user.username) or Ledger.objects.filter(receiver=request.user.username)
        count = transactions.count()

    except:
        transactions = ''
        count = 0
    return {'transactions': transactions, 'count': count}
