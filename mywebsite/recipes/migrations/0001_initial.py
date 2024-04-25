# Generated by Django 5.0.4 on 2024-04-13 21:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='recipesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=128)),
                ('meal_type', models.TextField(choices=[('BREAKFAST', 'Breakfast'), ('LUNCH', 'Lunch'), ('DINNER', 'Dinner'), ('DESSERT', 'Dessert'), ('APPETIZER', 'Appetizer')])),
                ('ingredients', models.CharField(max_length=2000)),
                ('instructions', models.CharField(max_length=2000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
