# Generated by Django 3.1.2 on 2021-11-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpmn', '0004_auto_20210812_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='diagram_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='event',
            name='diagram_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
