# Generated by Django 4.2.4 on 2023-09-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_alter_item_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
