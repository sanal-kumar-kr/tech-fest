# Generated by Django 5.0.4 on 2024-06-08 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth_app', '0029_alter_events_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='spostatus',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
