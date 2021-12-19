# Generated by Django 3.2.6 on 2021-12-19 11:16

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
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_boards', to='university.university')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
