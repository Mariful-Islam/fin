# Generated by Django 4.2.2 on 2023-08-29 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='transaction',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='base.transaction'),
        ),
    ]
