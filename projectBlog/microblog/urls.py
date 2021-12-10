from django.urls import path

from . import views

urlpatterns = [
    path('', views.project_overview, name='overview'),
    path('createPost', views.create_post, name='create_post'),
    path('<str:project_name>', views.project_timeline, name='timeline')
]
