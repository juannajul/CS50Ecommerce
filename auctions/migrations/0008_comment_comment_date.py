# Generated by Django 3.0.8 on 2020-12-08 16:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201204_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
