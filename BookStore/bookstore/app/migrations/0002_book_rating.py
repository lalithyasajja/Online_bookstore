# Generated by Django 4.2.3 on 2023-07-06 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
