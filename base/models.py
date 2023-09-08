from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

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
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    tran_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.receiver.username


class Transaction(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    tran_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    # def __str__(self):
    #     return self.transfer


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=8, unique=True)
    balance = models.FloatField()

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=8, unique=True)
    message = models.TextField()

    def __str__(self):
        return self.message


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username
