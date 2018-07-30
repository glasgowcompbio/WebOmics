# Generated by Django 2.0.2 on 2018-06-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0021_analysisannotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysisannotation',
            name='analysis_data',
        ),
        migrations.AddField(
            model_name='analysisannotation',
            name='data_type',
            field=models.IntegerField(choices=[(0, 'Genomics'), (1, 'Transcriptomics'), (2, 'Proteomics'), (3, 'Metabolomics'), (4, 'Reactions'), (5, 'Pathways')], default=0),
            preserve_default=False,
        ),
    ]