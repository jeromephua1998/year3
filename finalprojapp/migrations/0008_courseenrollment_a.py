# Generated by Django 3.0 on 2024-03-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalprojapp', '0007_remove_course_a'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseenrollment',
            name='a',
            field=models.CharField(default='a', max_length=100),
        ),
    ]
