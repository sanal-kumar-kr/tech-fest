# Generated by Django 5.0.4 on 2024-05-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_alter_registevevnts_evnt_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='registevevnts',
            name='card',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
