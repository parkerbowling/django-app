# Generated by Django 5.0.1 on 2024-03-15 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_budgetcategory_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensereport',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_reports', to='expenses.budgetcategory'),
        ),
    ]