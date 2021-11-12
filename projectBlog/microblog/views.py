from django.shortcuts import render
from django.urls import reverse
from urllib.parse import quote_plus, unquote_plus
from django.db.models import Max
from .models import BlogProject


def project_overview(request):
    projects = BlogProject.objects.all().annotate(latest_post=Max('posts__date')).order_by('-latest_post')
    return render(request, 'microblog/overview.html', context={
        "projects": [{"name": p.name,
                      "url": reverse('timeline', kwargs={"project_name": quote_plus(p.name)})}
                     for p in projects]
    })


def project_timeline(request, project_name):
    projects = BlogProject.objects.all().annotate(latest_post=Max('posts__date')).order_by('-latest_post')
    project = BlogProject.objects.filter(name=unquote_plus(project_name)).first()
    if project is None:
        return render(request, 'microblog/project_not_found.html', context={
            "project_name": project_name,
            "existing_projects": [{"name": p.name,
                                   "url": reverse('timeline', kwargs={"project_name": quote_plus(p.name)})}
                                  for p in projects]
        })
    posts = project.posts.all().order_by('date')
    return render(request, 'microblog/timeline.html', context={
        "project_list": [{
            "name": project.name,
            "url": "/{}".format(quote_plus(project.name))
        } for project in projects],
        "project_name": project.name,
        "posts": [{
            "date": post.date,
            "author": post.author.username if post.author is not None else "Arno Nym",
            "text": post.text
        } for post in posts]
    })
