# Generated by Django 5.0.3 on 2024-03-07 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth_app', '0011_remove_programs_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='programs',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Auth_app.category'),
        ),
    ]
