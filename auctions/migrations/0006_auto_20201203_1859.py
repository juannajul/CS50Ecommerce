# Generated by Django 3.0.8 on 2020-12-03 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auction_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='auction_watched',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='auction_watched',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auction_watched', to='auctions.Auction'),
            preserve_default=False,
        ),
    ]
