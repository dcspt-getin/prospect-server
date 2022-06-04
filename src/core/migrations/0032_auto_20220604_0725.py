# Generated by Django 3.1.4 on 2022-06-04 07:25

from django.db import migrations


def insert_configurations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Configuration = apps.get_model('core', 'Configuration')

    Configuration.objects.create(key='GOOGLE_API_KEY', value='')
    Configuration.objects.create(key='DEBUG_COMPARISIONS_MODEL', value='false')
    Configuration.objects.create(
        key='LIMIT_GOOGLE_API_CALLS_DAILY', value='10000')
    Configuration.objects.create(
        key='DEFAULT_SELECTED_TERRITORIAL_COVERAGE_ID', value='')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20220505_1111'),
    ]

    operations = [
        migrations.RunPython(insert_configurations, migrations.RunPython.noop)
    ]