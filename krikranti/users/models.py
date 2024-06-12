from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    desc = models.CharField(max_length=1000)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=50)
    Date_of_birth = models.CharField(max_length=25)
    citizenship = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users/images')


def __str__(self):
    return self.user.username
