from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.admin import ModelAdmin

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField("email address")

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.phone + ' ' + self.email
    

class UserAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name