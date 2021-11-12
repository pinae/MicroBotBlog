from django.contrib import admin
from .models import BlogProject, BlogPost, BlogImage

admin.site.register(BlogProject)
admin.site.register(BlogPost)
admin.site.register(BlogImage)
