from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length = 100)
    hall_number = models.CharField(max_length = 10)

class Guest(models.Model):
    name = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 13)

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name = 'reservation', on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, related_name = 'reservation', on_delete = models.CASCADE)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 144)
    body = models.TextField()


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)