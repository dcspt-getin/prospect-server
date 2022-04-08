# Generated by Django 3.1.4 on 2022-03-25 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20220321_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='show_previous_iteration',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='multiple_selection_type',
            field=models.CharField(blank=True, choices=[('RADIO', 'Radio'), ('SELECT', 'Select'), ('MULTIPLE_OPTIONS', 'Multiple')], default=None, max_length=30),
        ),
    ]