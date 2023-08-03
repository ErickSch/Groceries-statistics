from django.urls import path, include
from . import views



urlpatterns = [
    path("", views.statistics, name="statistics"),
    # path("lists/<str:primary_key_first_list>", views.lists, name="lists"),
]
