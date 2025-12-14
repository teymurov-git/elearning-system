from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

def get_current_year():
    return datetime.now().year

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


class MonthlyPayment(models.Model):
    MONTH_CHOICES = [
        (1, 'Yanvar'),
        (2, 'Fevral'),
        (3, 'Mart'),
        (4, 'Aprel'),
        (5, 'May'),
        (6, 'İyun'),
        (7, 'İyul'),
        (8, 'Avqust'),
        (9, 'Sentyabr'),
        (10, 'Oktyabr'),
        (11, 'Noyabr'),
        (12, 'Dekabr'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_payments', verbose_name='Tələbə')
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name='Ay')
    year = models.IntegerField(verbose_name='İl', default=get_current_year)
    is_paid = models.BooleanField(default=False, verbose_name='Ödəniş edilib')
    
    class Meta:
        unique_together = ('user', 'month', 'year')
        verbose_name = 'Aylıq Ödəniş'
        verbose_name_plural = 'Aylıq Ödənişlər'
        ordering = ['year', 'month']
    
    def __str__(self):
        month_name = dict(self.MONTH_CHOICES)[self.month]
        status = 'Ödənib' if self.is_paid else 'Ödənilməyib'
        return f"{self.user.first_name} {self.user.last_name} - {month_name} {self.year} ({status})"