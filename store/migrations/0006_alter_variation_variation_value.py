# Generated by Django 3.2.11 on 2024-10-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_variation_variation_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('black', 'Black'), ('white', 'White'), ('yellow', 'Yellow')], max_length=100),
        ),
    ]
