# Generated by Django 2.0.2 on 2018-06-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0005_analysisdata_analysisresult_analysissample'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='compound_reactions_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='compounds_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='gene_proteins_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='genes_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='pathways_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='protein_reactions_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='proteins_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='reaction_pathways_json',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='reactions_json',
        ),
        migrations.AlterField(
            model_name='analysisdata',
            name='data_type',
            field=models.IntegerField(choices=[(0, 'Genomics'), (1, 'Transcriptomics'), (2, 'Proteomics'), (3, 'Metabolomics'), (4, 'Reactions'), (5, 'Pathways'), (6, 'Genes to Proteins'), (7, 'Proteins to Reactions'), (8, 'Compounds to Reactions'), (9, 'Reaction to Pathways')]),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='data_type',
            field=models.IntegerField(choices=[(0, 'Genomics'), (1, 'Transcriptomics'), (2, 'Proteomics'), (3, 'Metabolomics'), (4, 'Reactions'), (5, 'Pathways')]),
        ),
    ]