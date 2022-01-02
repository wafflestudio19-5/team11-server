# Generated by Django 3.2.6 on 2021-12-28 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_auto_20211228_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'default'), (1, 'career'), (2, 'promotion'), (3, 'organization'), (4, 'department'), (5, 'general')], default=5),
        ),
    ]
