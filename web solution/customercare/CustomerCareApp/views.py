from django.shortcuts import render
from . import models
from email_generation_files import main_file as mf

def index(request, table_name=None):
    coloumn_name, table_data = models.view_database(table_name)
    return render(request, 'customercare_html/index.html', {
        'coloumn_name': coloumn_name,
        'table_data': table_data,
    })

def emailgeneration():
    while True:
        # try:
        mf.process_emails()
        # except Exception as e:
        # print("Error in processing emails:, e")
        import time
        time.sleep(5)
