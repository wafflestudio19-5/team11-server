# Generated by Django 3.2.6 on 2022-01-14 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0005_alter_lecture_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='location',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='time',
            field=models.CharField(max_length=300, null=True),
        ),
    ]