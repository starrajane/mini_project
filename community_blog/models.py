from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    post_created_timestamp = models.DateTimeField(auto_now_add=True)
    post_updated_timestamp = models.DateTimeField(auto_now=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', related_name='posts', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.content + ' by ' + self.author.username

class Comment(models.Model):
    post_id = models.ForeignKey(Post, models.DO_NOTHING)
    comment_content = models.TextField(max_length=5000)
    comment_created_timestamp = models.DateTimeField(auto_now_add=True)
    comment_updated_timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content


