# Generated by Django 4.2.4 on 2023-09-29 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0009_favoriteitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteitem',
            name='counter',
            field=models.IntegerField(default=1),
        ),
    ]