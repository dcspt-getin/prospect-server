# Generated by Django 3.1.4 on 2022-07-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20220719_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='territorial_coverages',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Territorial coverages (ids separated by comma)'),
        ),
    ]
