# Generated by Django 5.0.4 on 2024-06-08 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='decorations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec', models.FileField(null=True, upload_to='')),
                ('year', models.IntegerField(null=True)),
            ],
        ),
    ]
