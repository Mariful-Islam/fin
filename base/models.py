from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(unique=True, max_length=10)
    email = models.EmailField(unique=True, null=True)
    avater = models.ImageField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Transfer(models.Model):
    account_id = models.CharField(max_length=20)
    amount = models.FloatField()
    tran_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receiver.username


class Ledger(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=20, unique=True)
    balance = models.FloatField()

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_name(self):
        return self.user.name

    def get_email(self):
        return self.user.email

    def get_avater(self):
        return self.user.avater.url


class Revenue(models.Model):
    revenue = models.FloatField()
    gas_fee = models.FloatField()

    def __str__(self):
        revenue = str(self.revenue)
        return revenue
