# Generated by Django 5.1.5 on 2025-07-04 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
