# Generated by Django 3.1.6 on 2021-02-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bauabrechnung', '0002_auto_20210203_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coworker',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
