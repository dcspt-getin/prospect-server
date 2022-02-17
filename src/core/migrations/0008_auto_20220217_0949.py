# Generated by Django 3.1.4 on 2022-02-17 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220211_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='value_max',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='value_min',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Ativa'), ('NOT_ACTIVE', 'Desativa')], default='ACTIVE', max_length=30),
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.question'),
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='row_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Ativa'), ('NOT_ACTIVE', 'Desativa')], default='ACTIVE', max_length=30),
        ),
        migrations.CreateModel(
            name='GroupQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.groupquestions')),
            ],
            options={
                'permissions': (),
            },
        ),
        migrations.AddField(
            model_name='question',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.groupquestions'),
        ),
    ]
