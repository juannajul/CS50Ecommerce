# Generated by Django 3.0.8 on 2020-11-28 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_date_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
    ]