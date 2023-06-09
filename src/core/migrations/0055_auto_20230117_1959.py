# Generated by Django 3.1.4 on 2023-01-17 19:59


from django.db import migrations


def insert_configurations(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Configuration = apps.get_model('core', 'Configuration')

    Configuration.objects.create(key='ANONYMOUS_SESSION_MAX_TIME', value='')
    Configuration.objects.create(
        key='ANONYMOUS_SESSION_SHOW_ALERT_TIME', value='')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20230107_0942'),
    ]

    operations = [
        migrations.RunPython(insert_configurations, migrations.RunPython.noop)
    ]
