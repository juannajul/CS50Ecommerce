# Generated by Django 3.0.8 on 2020-11-27 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201123_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date_bid',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
