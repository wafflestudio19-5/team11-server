# Generated by Django 3.2.6 on 2022-01-14 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0004_auto_20220114_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='detail',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]