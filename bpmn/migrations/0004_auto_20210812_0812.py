# Generated by Django 3.1.2 on 2021-08-12 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpmn', '0003_ontology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagram',
            name='svg',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='diagram',
            name='xml',
            field=models.TextField(default=''),
        ),
    ]