# Generated by Django 3.1.4 on 2022-08-22 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housearch', '0002_auto_20220719_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='territorialcoverage',
            options={'permissions': (), 'verbose_name': 'Territorial Coverage', 'verbose_name_plural': 'Territorial Coverages'},
        ),
        migrations.AlterModelOptions(
            name='territorialunit',
            options={'permissions': (), 'verbose_name': 'Territorial Unit', 'verbose_name_plural': 'Territorial Units'},
        ),
        migrations.AlterModelOptions(
            name='territorialunitimage',
            options={'permissions': (), 'verbose_name': 'Territorial Unit Image', 'verbose_name_plural': 'Territorial Unit Images'},
        ),
    ]
