# Generated by Django 4.2.7 on 2023-11-24 11:01

from django.db import migrations
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', myapp.models.UserManager()),
            ],
        ),
    ]
