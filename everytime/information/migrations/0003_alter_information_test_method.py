# Generated by Django 3.2.6 on 2022-01-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_information_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='test_method',
            field=models.CharField(max_length=150),
        ),
    ]
