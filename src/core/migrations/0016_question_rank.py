# Generated by Django 3.1.4 on 2022-03-07 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20220307_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]