# Generated by Django 2.2.9 on 2020-02-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0038_auto_20190412_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysis',
            options={'verbose_name_plural': 'Analyses'},
        ),
        migrations.AlterModelOptions(
            name='analysisannotation',
            options={'verbose_name_plural': 'Analysis Annotations'},
        ),
        migrations.AlterModelOptions(
            name='analysisdata',
            options={'verbose_name_plural': 'Analysis Data'},
        ),
        migrations.AlterModelOptions(
            name='analysisgroup',
            options={'verbose_name_plural': 'Analysis Groups'},
        ),
        migrations.RenameField(
            model_name='analysis',
            old_name='user',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='analysisdata',
            name='inference_type',
            field=models.IntegerField(blank=True, choices=[(None, '-'), (0, 'Differential Expression Analysis (t-test)'), (6, 'Differential Expression Analysis (DESeq2)'), (7, 'Differential Expression Analysis (limma)'), (2, 'Principal Component Analysis (PCA)'), (3, 'Pathway Analysis (PLAGE)'), (4, 'Pathway Analysis (ORA)'), (5, 'Pathway Analysis (GSEA)')], null=True),
        ),
    ]
