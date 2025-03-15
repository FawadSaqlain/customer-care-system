from django.shortcuts import render
from . import models
from email_generation_files import main_file as mf


def index(request, table_name=None):
    # Default to "Employees" if no valid table name is provided (or if it's an unwanted request like favicon.ico)
    # if not table_name or table_name.lower() == "favicon.ico":
    #     table_name = "Employees"
    coloumn_name, table_data = models.view_database(table_name)
    mf.process_emails()
    return render(request, 'customercare_html/index.html', {
        'coloumn_name': coloumn_name,
        'table_data': table_data,
    })
