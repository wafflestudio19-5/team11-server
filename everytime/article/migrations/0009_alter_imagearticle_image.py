# Generated by Django 3.2.6 on 2022-01-06 14:09

from django.db import migrations, models
import user.utils


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_alter_article_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagearticle',
            name='image',
            field=models.ImageField(editable=False, upload_to=user.utils.upload_image),
        ),
    ]
