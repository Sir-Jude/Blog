# Generated by Django 5.0.9 on 2024-10-16 08:10

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
    ]