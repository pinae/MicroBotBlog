from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from urllib.parse import quote_plus, unquote_plus
from django.db.models import Max
from .models import BlogProject, BlogPost, BlogImage
from django.contrib.auth.models import User
from json import loads
from requests import get
from PIL import Image


class BadRequestException(Exception):
    pass


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


def get_author(data):
    if "author_info" not in data:
        raise BadRequestException("Error: \"author_info\" is missing.")
    author_info = data["author_info"]
    if "first_name" not in author_info or "last_name" not in author_info:
        raise BadRequestException("Error: \"author_info\" is incomplete. " +
                        "It must have a \"first_name\" and a \"last_name\".")
    try:
        user = User.objects.get(first_name=author_info["first_name"], last_name=author_info["last_name"])
    except User.DoesNotExist:
        raise BadRequestException("There is no User {} {}.".format(
            author_info["first_name"], author_info["last_name"]))
    return user


def get_project(data):
    if "project_name" not in data:
        raise BadRequestException("Error: \"project_name\" is missing.")
    project_name = data["project_name"]
    try:
        project = BlogProject.objects.get(name=project_name)
    except BlogProject.DoesNotExist:
        raise BadRequestException("There is not BlogProject with the name \"{}\".".format(project_name))
    return project


def get_or_make_post(data, project, author):
    telegram_id = None
    if "telegram_id" in data:
        telegram_id = data["telegram_id"]
        try:
            post = BlogPost.objects.get(project=project, author=author, telegram_id=telegram_id)
        except BlogPost.DoesNotExist:
            post = BlogPost(project=project, author=author, telegram_id=telegram_id)
    else:
        post = BlogPost(project=project, author=author, telegram_id=telegram_id)
    return post


def create_post(request):
    data = loads(request.body)
    try:
        user = get_author(data)
    except BadRequestException as e:
        return HttpResponseBadRequest(str(e))
    try:
        project = get_project(data)
    except BadRequestException as e:
        return HttpResponseBadRequest(str(e))
    if "text" not in data:
        return HttpResponseBadRequest("Error: \"text\" is missing.")
    text = data["text"]
    post = get_or_make_post(data, project, author=user)
    post.text = text
    post.save()
    return HttpResponse("OK")


def download_image(request):
    data = loads(request.body)
    try:
        user = get_author(data)
    except BadRequestException as e:
        return HttpResponseBadRequest(str(e))
    try:
        project = get_project(data)
    except BadRequestException as e:
        return HttpResponseBadRequest(str(e))
    post = get_or_make_post(data, project, author=user)
    if "caption" not in data:
        return HttpResponseBadRequest("Error: \"caption\" is missing.")
    post.text = data["caption"]
    post.save()
    for i, image_url in enumerate(data['album']):
        img_stream = get(image_url, stream=True)
        img_stream.raw.decode_content = True  # unzip automatically if the response is compressed
        with Image.open(img_stream.raw) as img:
            blog_image = BlogImage(image=img, post=post)
            blog_image.save()
        post.text = "[{}{}]({}{})\n\n{}".format(
            data["caption"],
            " - Image No. " + str(i) if len(data['album']) > 1 else "",
            settings.MEDIA_URL,
            blog_image.image.url(),
            post.text)
    post.save()
