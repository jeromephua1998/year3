# Generated by Django 3.0 on 2024-02-29 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalprojapp', '0005_auto_20240227_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='a',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
