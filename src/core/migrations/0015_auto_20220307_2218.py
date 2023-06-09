# Generated by Django 3.1.4 on 2022-03-07 22:18

from django.db import migrations


def insert_configurations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Configuration = apps.get_model('core', 'Configuration')

    Configuration.objects.create(key='SHOW_PREVIOUS_QUESTION', value='false')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20220307_2210'),
    ]

    operations = [
        migrations.RunPython(insert_configurations, migrations.RunPython.noop)
    ]
