from django.urls import path, include
from . import views



urlpatterns = [
    path("", views.manager, name="manager"),
    path("project/<str:primary_key_project>/", views.project, name="project"),
    path("project/<str:primary_key_project>/process/<str:primary_key_process>/", views.process, name="process"),
    path("project/<str:primary_key_project>/process/<str:primary_key_process>/edit_activity/<str:primary_key_activity>/", views.edit_activity, name="edit_activity"),
    path("project/delete_project/<str:primary_key_project>/", views.delete_project, name="delete_project"),
    path("project/<str:primary_key_project>/process/delete_process/<str:primary_key_process>/", views.delete_process, name="delete_process"),
    path("project/<str:primary_key_project>/process/<str:primary_key_process>/activity/delete_activity/<str:primary_key_activity>/", views.delete_activity, name="delete_activity"),

]
