# Generated by Django 3.1.4 on 2022-08-06 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20220720_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='use_google_street_images',
            field=models.BooleanField(default=True, verbose_name='Show Google Street Images'),
        ),
    ]
