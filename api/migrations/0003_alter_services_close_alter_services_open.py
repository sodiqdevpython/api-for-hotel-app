# Generated by Django 5.0.4 on 2024-04-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_clode_services_close'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='close',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='services',
            name='open',
            field=models.CharField(max_length=10),
        ),
    ]
