# Generated by Django 3.1.4 on 2023-01-04 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='header_menu',
            field=models.BooleanField(default=False, verbose_name='Visible on header menu'),
        ),
    ]
