# Generated by Django 4.1.dev20211105111118 on 2021-12-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0002_blogimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='telegram_id',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
