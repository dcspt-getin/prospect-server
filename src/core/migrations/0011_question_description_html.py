# Generated by Django 3.1.4 on 2022-02-22 22:42

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description_html',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
