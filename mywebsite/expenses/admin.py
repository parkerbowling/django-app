from django.contrib import admin
from .models import expenseReport

#this just registers the table so I can see it in the admin page
admin.site.register(expenseReport)