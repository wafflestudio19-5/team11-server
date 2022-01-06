# Generated by Django 3.2.6 on 2022-01-05 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20211231_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('description', models.CharField(max_length=5000, null=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_article', to='article.article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
