# Generated by Django 3.2.6 on 2021-12-28 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(default='general', max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('allow_anonymous', models.BooleanField(default=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='boards', to='university.university')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
