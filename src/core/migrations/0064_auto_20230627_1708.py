# Generated by Django 3.1.4 on 2023-06-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_question_embedded_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='embedded_question_url',
            field=models.CharField(blank=True, max_length=268, null=True, verbose_name='Embeded Question External Url'),
        ),
    ]
