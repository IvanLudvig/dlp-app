# Generated by Django 4.0.4 on 2022-04-16 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
