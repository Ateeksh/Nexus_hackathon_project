# Generated by Django 5.1.5 on 2025-01-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fit_AI', '0002_rename_protien_user_protein_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
