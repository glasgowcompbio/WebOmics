# Generated by Django 2.0.2 on 2018-06-25 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0016_auto_20180625_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisUploadSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='analysisupload',
            name='species',
            field=models.ManyToManyField(to='linker.AnalysisUploadSpecies'),
        ),
    ]
