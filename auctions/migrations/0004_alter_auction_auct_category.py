# Generated by Django 3.2.8 on 2021-10-18 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211018_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auct_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.category'),
        ),
    ]
