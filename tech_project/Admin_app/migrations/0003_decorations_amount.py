# Generated by Django 5.0.4 on 2024-06-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0002_decorations'),
    ]

    operations = [
        migrations.AddField(
            model_name='decorations',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
