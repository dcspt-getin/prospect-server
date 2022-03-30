# Generated by Django 3.1.4 on 2022-03-15 11:25

from django.db import migrations


def insert_configurations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Configuration = apps.get_model('core', 'Configuration')

    Configuration.objects.create(
        key='ALLOW_USER_REPEAT_BALANCE_QUESTION', value='false')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20220315_1054'),
    ]

    operations = [
        migrations.RunPython(insert_configurations, migrations.RunPython.noop)
    ]
