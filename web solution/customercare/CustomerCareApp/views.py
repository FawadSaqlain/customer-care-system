# views.py
from django.shortcuts import render
from . import models

def index(request, table_name=None):
    # If no table name is provided, pick one or just return an empty table
    if not table_name:
        table_name = "Employees"  # or any default

    coloumn_name, table_data = models.view_database(table_name)
    return render(request, 'customercare_html/index.html', {
        'coloumn_name': coloumn_name,
        'table_data': table_data
    })
