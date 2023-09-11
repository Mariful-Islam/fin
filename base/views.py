from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserForm, ProfileForm, BankAccountForm, TransferForm
from .models import User, Transaction, Transfer, Profile, BankAccount, Message


# Create your views here.

def home(request):
    transaction = Transaction.objects.all()
    # connect =
    # message =

    context = {'transaction': transaction}
    return render(request, 'index.html')


def transfer(request):
    if request.method == "POST":
        account_id = request.POST['accountid']
        amount = request.POST['amount']
        try:
            receiver_account = BankAccount.objects.get(
                account_id=account_id)
            receiver = receiver_account.user

            transfer = Transfer.objects.create(
                receiver=receiver, amount=amount)
            transaction = Transaction.objects.create(transfer=transfer)

            transfer.save()
            transaction.save()

            # balance system
            try:
                sender_account = BankAccount.objects.get(user=request.user)
                sender_account.balance = sender_account.balance-float(amount)
                receiver_account.balance = receiver_account.balance + \
                    float(amount)

                sender_account.save()
                receiver_account.save()

                messages.info(
                    request, 'You successfully sent {}$ to {}.'.format(amount, receiver))
            except:
                messages.info(request, 'Balance not updated')

            # print(new_sender_balance, new_receiver_balance, amount)

            # sender_account.objects.(balance=new_sender_balance)
            # receiver_account.objects.update(balance=new_receiver_balance)

        except:
            messages.info(request, 'No User Found')
        return redirect('transfer')

    return render(request, 'transfer.html')


def friend_transfer(request, account_id):
    if request.method == "POST":
        account_id = request.POST['accountid']
        amount = request.POST['amount']
        try:
            receiver_account = BankAccount.objects.get(account_id=account_id)
            receiver = receiver_account.user

            transfer = Transfer.objects.create(
                receiver=receiver, amount=amount)
            transaction = Transaction.objects.create(transfer=transfer)

            transfer.save()
            transaction.save()

            try:
                sender_account = BankAccount.objects.get(user=request.user)
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

    context = {'account_id': account_id}
    return render(request, 'friend-transfer.html', context)


def transaction(request):

    trans = Transaction.objects.all()
    if not trans:
        messages.info(request, 'No transaction ')
    return render(request, 'transaction.html', {'trans': trans})


def balance(request, username):
    try:
        user = User.objects.get(username=username)
        balance = BankAccount.objects.get(user=user).balance
    except:
        balance = 0

    context = {'balance': balance}
    return render(request, 'balance.html', context)


def friends(request):
    accounts = BankAccount.objects.all()
    context = {'accounts': accounts}
    return render(request, 'friends.html', context)


def message(request):
    user = User.objects.get(username=request.user.username)
    messages = Message.objects.filter(user=user)
    if request.method == "POST":
        user = request.user.username

        message = request.POST['message']
        sent_message = Message.objects.create(user=user, message=message)
        sent_message.save()

    context = {'user': user, 'messages': messages}
    return render(request, 'message.html', context)


def notification(request):

    try:
        user = User.objects.get(username=request.user.username)
        messages = Message.objects.get(user=user)
        bank_account = BankAccount.objects.get(user=user)
        transfer = Transfer.objects.get(receiver=user)
        transactions = Transaction.objects.get(transfer=transfer)
    except:
        messages = ''
        transactions = ''

    context = {'user': user, 'messages': messages,
               'transactions': transactions}
    return render(request, 'notification.html', context)


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

    context = {'previous_bank_account': previous_bank_account,
               'user': user, 'profile': profile, 'username': username}
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
        return redirect('profile')

    return render(request, 'bank-account.html')


def setting(request):
    return render(request, 'setting.html')


def edit_user(request, username):
    user = User.objects.get(username=username)
    form = CustomUserForm(instance=user)
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'edit-user.html', context)


def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'edit-profile.html', context)


def log_in(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Username does not existed')

        user = User.objects.filter(email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
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

    context = {'form': form}
    return render(request, 'signup.html', context)


def log_out(request):
    logout(request)
    return redirect('/')
