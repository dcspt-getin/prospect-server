# Generated by Django 3.1.4 on 2022-02-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220211_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionoption',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
