# Generated by Django 4.0 on 2021-12-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playergame',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
