# Generated by Django 3.1.4 on 2022-04-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20220330_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='checkbox_max_options',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='checkbox_min_options',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
