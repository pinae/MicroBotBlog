from django.urls import path

from . import views

urlpatterns = [
    path('', views.project_overview, name='overview'),
    path('<str:project_name>', views.project_timeline, name='timeline')
]
