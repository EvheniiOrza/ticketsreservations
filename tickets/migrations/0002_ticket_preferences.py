# Generated by Django 5.1.3 on 2024-11-18 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='preferences',
            field=models.TextField(blank=True, null=True),
        ),
    ]
