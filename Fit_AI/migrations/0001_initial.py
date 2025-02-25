# Generated by Django 5.1.5 on 2025-01-20 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Excersise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('Reps', models.DecimalField(decimal_places=0, max_digits=2)),
                ('Sets', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Timeperrep', models.PositiveIntegerField()),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('calories', models.IntegerField()),
                ('protein', models.FloatField()),
                ('eaten', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('access', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('usage', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight_goal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Medical_history', models.TextField()),
                ('Additional_information', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fitness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('excersise', models.ManyToManyField(related_name='fitness_exercises', to='Fit_AI.excersise')),
                ('diet', models.ManyToManyField(related_name='fitness_diets', to='Fit_AI.fooditem')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('steps', models.DecimalField(decimal_places=0, default=0, max_digits=5)),
                ('sleep', models.DecimalField(decimal_places=0, default=0, max_digits=2)),
                ('calories', models.DecimalField(decimal_places=0, default=0, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('protien', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('Excersise_done', models.ManyToManyField(related_name='excersise', to='Fit_AI.fooditem')),
                ('food', models.ManyToManyField(related_name='diets', to='Fit_AI.fooditem')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='Fit_AI.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('steps', models.DecimalField(decimal_places=0, max_digits=5)),
                ('sleep', models.DecimalField(decimal_places=0, max_digits=2)),
                ('calories', models.DecimalField(decimal_places=0, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('protien', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='Fit_AI.user')),
            ],
        ),
    ]
