from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransferSerializer, BankAccountSerializer, LedgerSerializer, UserSerializer, ProfileSerializer, RevenueSerializer
from django.contrib import messages
from base.models import Ledger, Revenue, User, Transfer, BankAccount, Profile
from base.utils import get_transaction, get_transfer, transaction_id_generator
from django.contrib.auth import authenticate, login, logout
# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def getRouter(request):
    data = {
        "content": "Welcome to Fin API"
    }
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def sign_up(request):
    if request.method == "POST":
        name = request.data['name']
        username = request.data['username']
        email = request.data['email']
        avater = request.data['avater']
        password1 = request.data['password1']
        password2 = request.data['password2']

        User.objects.create(name=name,
                            username=username,
                            email=email,
                            avater=avater,
                            password1=password1,
                            password2=password2)

    return Response()


@api_view(['GET', 'POST'])
def log_in(request):
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not existed')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return Response({'login_success': 'success'})
        else:
            return Response({'login_failed': 'failed'})


@api_view(['GET', 'POST'])
def transfer(request):
    if request.method == 'POST':
        account_id = request.data['account_id']
        amount = request.data['amount']

        receiver_account = BankAccount.objects.get(account_id=account_id).user

        Transfer.objects.create(
            account_id=account_id,
            amount=amount,
        )

        Ledger.objects.create(
            sender=request.user.username,
            receiver=receiver_account.username,
            amount=amount,
            transaction_id=transaction_id_generator()
        )

    transfers = Transfer.objects.all()
    serializer = TransferSerializer(transfers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transactions(request):
    context = get_transaction(request)
    transactions = context['transactions']

    serializer = LedgerSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ledger(request):
    ledgers = Ledger.objects.all()

    serializer = LedgerSerializer(ledgers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def balance(request):
    try:
        user = User.objects.get(username=request.user.username)
        balance = BankAccount.objects.get(user=user).balance
    except:
        balance = 0

    return Response({'balance': balance})


@api_view(['GET'])
def friends(request):
    accounts = BankAccount.objects.all()
    # accounts = BankAccount.objects.exclude(user=request.user)

    data = get_transaction(request)
    count = data['count']
    serializer = BankAccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def create_bank_account(request):
    if request.method == "POST":
        account_id = request.data['account_id']
        balance = request.data['balance']
        BankAccount.objects.create(
            user=request.user,
            account_id=account_id,
            balance=balance
        )

    return Response()


@api_view(['GET'])
def get_bank_account(request, username):
    user = User.objects.get(username=username)
    account = BankAccount.objects.get(user=user)
    serializer = BankAccountSerializer(account, many=False)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def create_profile(request):
    if request.method == "POST":
        address = request.data['address']
        bio = request.data['bio']

        Profile.objects.create(user=request.user, address=address, bio=bio)

    return Response('Profile Created')


@api_view(['GET'])
def get_profile(request, username):
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = ''

    profile_serializer = ProfileSerializer(profile)
    return Response(profile_serializer.data)


@api_view(['GET'])
def revenue(request):
    revenue = Revenue.objects.get(id=1)
    serializer = RevenueSerializer(revenue, many=False)
    return Response(serializer.data)
