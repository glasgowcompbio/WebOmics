# Generated by Django 2.0 on 2018-07-06 12:40

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0028_analysissample_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisdata',
            name='json_design',
            field=jsonfield.fields.JSONField(default=''),
            preserve_default=False,
        ),
    ]
