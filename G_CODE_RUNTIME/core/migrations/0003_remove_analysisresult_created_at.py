# Generated by Django 5.1.6 on 2025-03-01 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_analysisresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysisresult',
            name='created_at',
        ),
    ]
