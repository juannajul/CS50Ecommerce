# Generated by Django 3.0.8 on 2020-12-17 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201216_2223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-bid']},
        ),
    ]