# Generated by Django 4.2.2 on 2023-09-11 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='transaction_id',
            field=models.CharField(max_length=30),
        ),
    ]
