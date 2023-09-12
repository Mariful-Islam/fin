from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Transfer)
admin.site.register(Transaction)
admin.site.register(Ledger)
admin.site.register(BankAccount)
admin.site.register(Message)
admin.site.register(Profile)
