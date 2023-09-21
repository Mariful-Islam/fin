from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Transfer)
admin.site.register(Ledger)
admin.site.register(BankAccount)
admin.site.register(Profile)
admin.site.register(Revenue)
