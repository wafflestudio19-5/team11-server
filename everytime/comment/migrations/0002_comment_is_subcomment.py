# Generated by Django 3.2.6 on 2021-12-30 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_subcomment',
            field=models.BooleanField(default=False),
        ),
    ]
