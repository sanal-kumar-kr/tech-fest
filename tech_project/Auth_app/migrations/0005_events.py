# Generated by Django 5.0.3 on 2024-03-06 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth_app', '0004_programs_duration_programs_ptime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=500)),
                ('sdate', models.DateField(null=True)),
                ('edate', models.DateField(null=True)),
            ],
        ),
    ]
