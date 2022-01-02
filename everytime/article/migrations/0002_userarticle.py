# Generated by Django 3.2.6 on 2021-12-30 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=False)),
                ('scrap', models.BooleanField(default=False)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_article', to='article.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_article', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
