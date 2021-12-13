from django.urls import path

from . import views

urlpatterns = [
    path('', views.project_overview, name='overview'),
    path('createPost', views.create_post, name='create_post'),
    path('createImagePost', views.download_image, name='download_image'),
    path('<str:project_name>', views.project_timeline, name='timeline')
]
