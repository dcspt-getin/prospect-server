# Generated by Django 3.1.4 on 2022-04-06 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20220404_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupquestions',
            name='is_visible_on_results',
            field=models.BooleanField(default=False),
        ),
    ]