# Generated by Django 2.0.2 on 2018-06-12 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='timestamp',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
