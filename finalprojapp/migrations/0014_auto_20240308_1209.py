# Generated by Django 3.0 on 2024-03-08 12:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalprojapp', '0013_fileupload_courseid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusupdate',
            name='status',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(200)]),
        ),
    ]
