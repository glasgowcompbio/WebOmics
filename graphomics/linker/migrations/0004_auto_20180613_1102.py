# Generated by Django 2.0.2 on 2018-06-13 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0003_auto_20180613_1019'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Experiment',
            new_name='Analysis',
        ),
    ]
