# Generated by Django 2.2 on 2019-04-12 12:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('linker', '0036_auto_20181017_0222'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection_state', jsonfield.fields.JSONField()),
                ('display_name', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='linker.Analysis')),
            ],
        ),
    ]
