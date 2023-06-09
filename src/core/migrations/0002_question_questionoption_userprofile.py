# Generated by Django 3.1.4 on 2022-02-11 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=60, null=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('image_url', models.CharField(blank=True, max_length=60)),
                ('question_type', models.CharField(choices=[('MULTIPLE_CHOICE', 'Escolha múltipla'), ('SHORT_ANSWER', 'Resposta curta'), ('PAIRWISE_COMBINATIONS', 'Combionações par a par')], default=None, max_length=60)),
                ('default_value', models.CharField(blank=True, max_length=256)),
                ('input_type', models.CharField(blank=True, max_length=60)),
                ('status', models.CharField(choices=[('ACTIVE', 'Ativada'), ('NOT_ACTIVE', 'Desativada')], default='ACTIVE', max_length=30)),
            ],
            options={
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_data', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
            ],
            options={
                'permissions': (),
            },
        ),
    ]
