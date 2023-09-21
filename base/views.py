import csv
import os
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserForm, ProfileForm
from .models import Revenue, User, Profile, BankAccount, Ledger
import json
from django.conf import settings
from django.http import Http404, HttpResponse
from .utils import get_transfer, get_transaction, account_id_generator, get_service_charge
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.


def home(request):
    context = get_transaction(request)

    return render(request, 'index.html', context)


def transfer(request):
    get_transfer(request)

    gas_fee = Revenue.objects.get(id=1).gas_fee

    data = get_transaction(request)
    count = data['count']

    return render(request, 'transfer.html', {'count': count,
                                             "gas_fee": gas_fee})


def friend_transfer(request, account_id):
    get_transfer(request)

    gas_fee = Revenue.objects.get(id=1).gas_fee

    data = get_transaction(request)
    count = data['count']

    context = {'account_id': account_id, 'count': count, 'gas_fee': gas_fee}
    return render(request, 'friend-transfer.html', context)


def transaction(request):
    context = get_transaction(request)

    csv_file = open(
        'static/files/Transactions-{}.csv'.format(request.user.username), 'w', newline='')
    writter = csv.writer(csv_file)
    writter.writerow(
        ['Sender', 'Receiver', 'Amount', 'Transaction ID', 'Time'])
    for transaction in context['transactions']:
        sender = transaction.sender
        receiver = transaction.receiver
        amount = transaction.amount
        transaction_id = transaction.transaction_id
        time = transaction.time

        print(sender, receiver, amount, transaction_id, time)

        row = [sender, receiver, amount, transaction_id, time]
        writter.writerow(row)

    csv_file.close()

    return render(request, 'transaction.html', context)


def ledger(request):
    ledgers = Ledger.objects.all()

    data = get_transaction(request)
    count = data['count']
    no_ledger = ''

    csv_file = open('static/files/ledger.csv', 'w', newline='')
    writter = csv.writer(csv_file)
    writter.writerow(
        ['Sender', 'Receiver', 'Amount', 'Transaction ID', 'Time'])
    for ledger in ledgers:
        sender = ledger.sender
        receiver = ledger.receiver
        amount = ledger.amount
        transaction_id = ledger.transaction_id
        time = ledger.time

        print(sender, receiver, amount, transaction_id, time)

        row = [sender, receiver, amount, transaction_id, time]
        writter.writerow(row)

    csv_file.close()

    if not ledgers:
        no_ledger = 'No Ledger Found'

    context = {'ledgers': ledgers, 'count': count, 'no_ledger': no_ledger}
    return render(request, 'ledger.html', context)


def balance(request, username):
    try:
        user = User.objects.get(username=username)
        balance = BankAccount.objects.get(user=user).balance
    except:
        balance = 0

    data = get_transaction(request)
    count = data['count']

    context = {'balance': balance, 'count': count}
    return render(request, 'balance.html', context)


def friends(request):

    accounts = BankAccount.objects.all()
    accounts = BankAccount.objects.exclude(user=request.user)

    data = get_transaction(request)
    count = data['count']

    context = {'accounts': accounts, 'count': count}
    return render(request, 'friends.html', context)


def profile(request, username):
    user = User.objects.get(username=username)
    try:
        previous_bank_account = BankAccount.objects.get(user=user)
    except:
        previous_bank_account = ''
        messages.info(
            request, 'Hello Mr. {}, you have no bank account.'.format(username))
        return render(request, 'profile.html')

    try:
        user = User.objects.get(username=username)
    except:
        user = ''
        messages.info(request, 'No User Details Show')

    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = ''
        messages.info(request, 'No Profile Details Show')

    data = get_transaction(request)
    count = data['count']

    context = {'previous_bank_account': previous_bank_account,
               'user': user, 'profile': profile, 'username': username,
               'count': count}
    return render(request, 'profile.html', context)


def bank_account(request):

    if request.method == "POST":
        account_id = request.POST['account_id']
        balance = request.POST['balance']
        bank_account = BankAccount.objects.create(
            user=request.user,
            account_id=account_id,
            balance=balance
        )
        bank_account.save()
        messages.info(
            request, 'Hey ! Mr. {}, Your bank account successfully created.'.format(request.user.username))
        return redirect('profile', username=request.user.username)

    data = get_transaction(request)
    count = data['count']

    return render(request, 'bank-account.html', {'count': count,
                                                 'account_id': account_id_generator()})


def setting(request):

    data = get_transaction(request)
    count = data['count']

    return render(request, 'setting.html', {'count': count})


def edit_user(request, username):
    user = User.objects.get(username=username)
    form = CustomUserForm(instance=user)
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

    data = get_transaction(request)
    count = data['count']

    context = {'form': form, 'count': count}
    return render(request, 'edit-user.html', context)


def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    data = get_transaction(request)
    count = data['count']

    context = {'form': form, 'count': count}
    return render(request, 'edit-profile.html', context)


def log_in(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not existed')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    data = get_transaction(request)
    count = data['count']

    context = {'page': page, 'count': count}
    return render(request, 'login.html', context)


def signup(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error in Registration !!!')

    data = get_transaction(request)
    count = data['count']

    context = {'form': form, 'count': count}
    return render(request, 'signup.html', context)


def log_out(request):
    logout(request)
    return redirect('/')


def developer(request):

    data = get_transaction(request)
    count = data['count']

    return render(request, 'developer.html', {'count': count})


@login_required
@permission_required('is-superuser')
def gas_fee_update(request):
    revenue = Revenue.objects.get(id=1)

    previous_gas_fee = revenue.gas_fee
    if request.method == "POST":
        updated_gas_fee = request.POST['gas_fee']

        revenue.gas_fee = updated_gas_fee
        revenue.save()
        return redirect('home')

    return render(request, 'update-gas-fee.html', {'previous_gas_fee': previous_gas_fee})
