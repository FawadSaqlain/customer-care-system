from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:table_name>/", views.index, name="index_with_table"),
]
