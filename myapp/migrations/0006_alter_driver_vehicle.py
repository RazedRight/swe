# Generated by Django 4.2.7 on 2023-11-27 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_driver_driving_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.vehicle'),
        ),
    ]
