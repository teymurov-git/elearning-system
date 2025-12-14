from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField("email address")
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name='Group')

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.phone + ' ' + self.email


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name