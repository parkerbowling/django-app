# Generated by Django 5.0.1 on 2024-03-13 22:51

import django.db.models.deletion
import django.utils.timezone
import expenses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='expenseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=128)),
                ('value', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('note', models.TextField(max_length=140)),
                ('category', models.ForeignKey(default=expenses.models.get_or_create_default_category, on_delete=django.db.models.deletion.CASCADE, related_name='expense_reports', to='expenses.budgetcategory')),
            ],
        ),
    ]
