# Generated by Django 4.0 on 2023-07-18 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(default=None),
        ),
    ]