# Generated by Django 4.1.3 on 2022-11-11 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polluser',
            old_name='user_id',
            new_name='id',
        ),
    ]
