# Generated by Django 3.1.4 on 2022-07-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20220714_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image_pairwise_type',
            field=models.CharField(blank=True, choices=[('BINARY_CHOICE', 'Escolha Binária'), ('WEIGHT_BASED_CHOICE', 'Escolha com base em pesos')], default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='show_balance',
            field=models.BooleanField(default=True, verbose_name='Show balance (If applicable)'),
        ),
    ]
