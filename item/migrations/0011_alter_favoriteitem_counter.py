# Generated by Django 4.2.4 on 2023-09-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_favoriteitem_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteitem',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]