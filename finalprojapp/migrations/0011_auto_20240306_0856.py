# Generated by Django 3.0 on 2024-03-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalprojapp', '0010_statusupdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fileupload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='documents/%Y/%m/%d/')),
                ('timeuploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='status',
            field=models.TextField(max_length=50),
        ),
    ]
