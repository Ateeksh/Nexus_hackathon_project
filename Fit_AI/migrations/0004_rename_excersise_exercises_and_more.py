# Generated by Django 5.1.5 on 2025-01-22 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Fit_AI', '0003_remove_user_user_profile_user_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Excersise',
            new_name='Exercises',
        ),
        migrations.RenameField(
            model_name='fitness',
            old_name='excersise',
            new_name='exercise',
        ),
    ]
