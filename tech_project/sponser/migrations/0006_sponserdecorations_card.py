# Generated by Django 5.0.4 on 2024-06-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponser', '0005_remove_sponserdecorations_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponserdecorations',
            name='card',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
