# Generated by Django 5.0.4 on 2024-06-20 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponser', '0004_sponserdecorations_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponserdecorations',
            name='status',
        ),
    ]
