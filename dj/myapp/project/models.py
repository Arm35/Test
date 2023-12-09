from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Test(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    archive = models.IntegerField(default=0)


class Question(models.Model):
    question = models.CharField(max_length=100)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions", default=None, null=True)


class Answer(models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

class TestRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test")
    rating = models.IntegerField(default=0)