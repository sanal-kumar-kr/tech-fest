# Generated by Django 5.0.3 on 2024-03-07 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth_app', '0009_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='event_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Auth_app.events'),
        ),
    ]
