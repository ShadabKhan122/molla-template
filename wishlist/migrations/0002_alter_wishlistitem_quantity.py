# Generated by Django 3.2.11 on 2024-09-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
