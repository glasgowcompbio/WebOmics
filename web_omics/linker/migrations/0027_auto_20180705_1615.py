# Generated by Django 2.0 on 2018-07-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0026_auto_20180703_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysissample',
            old_name='group_name',
            new_name='level',
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='inference_type',
            field=models.IntegerField(choices=[(None, '-'), (0, 't-test'), (4, 'Hierarchical Clustering')]),
        ),
    ]
