# Generated by Django 3.2.8 on 2021-10-18 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_auct_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
