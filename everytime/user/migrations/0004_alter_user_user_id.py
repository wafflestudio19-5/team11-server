# Generated by Django 3.2.6 on 2021-12-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20211223_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
