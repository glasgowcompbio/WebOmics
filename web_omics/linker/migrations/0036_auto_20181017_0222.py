# Generated by Django 2.1.1 on 2018-10-17 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0035_auto_20181009_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisdata',
            name='display_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
