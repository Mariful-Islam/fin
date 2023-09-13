from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CustomUserForm, ProfileForm
from .models import User, Transaction, Transfer, Profile, BankAccount, Ledger
import json

from .utils import get_transfer, get_transaction

# Create your views here.


def home(request):
    data = get_transaction(request)
    count = data['count']

    context = {'count': count}
    return render(request, 'index.html', context)


def transfer(request):
    get_transfer(request)

    data = get_transaction(request)
    count = data['count']

    return render(request, 'transfer.html', {'count': count})


def friend_transfer(request, account_id):
    get_transfer(request)

    data = get_transaction(request)
    count = data['count']

    context = {'account_id': account_id, 'count': count}
    return render(request, 'friend-transfer.html', context)


def transaction(request):
    data = get_transaction(request)
    transactions = data['transactions']
    count = data['count']

    return render(request, 'transaction.html', {'transactions': transactions, 'count': count})


def ledger(request):
    ledgers = Ledger.objects.all()

    data = get_transaction(request)
    count = data['count']

    context = {'ledgers': ledgers, 'count': count}
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

    return render(request, 'bank-account.html', {'count': count})


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
