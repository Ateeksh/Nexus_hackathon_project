# Generated by Django 5.1.5 on 2025-01-22 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fit_AI', '0006_alter_user_sleep_alter_usergoals_protein_goal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sleep',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='usergoals',
            name='sleep_goal',
            field=models.DecimalField(decimal_places=0, default=8.0, max_digits=2),
        ),
    ]
