from django.db import models
from django.conf import settings
from django.utils import timezone


class BlogProject(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    project = models.ForeignKey(BlogProject,
                                on_delete=models.CASCADE,
                                related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='posts')
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    telegram_id = models.IntegerField(null=True, default=None)

    def __str__(self):
        return "{}: {}...".format(self.project.name, self.text[:100])


class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost,
                             on_delete=models.CASCADE,
                             related_name='images')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.image)
