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
    work_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='İş Nömrəsi')

    class Meta:
        verbose_name = 'Tələbə' 
        verbose_name_plural = 'Tələbələr'

    def __str__(self):
        first_name = self.first_name or ''
        last_name = self.last_name or ''
        phone = self.phone or ''
        email = self.email or ''
        return f"{first_name} {last_name} {phone} {email}".strip()


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=200, verbose_name='Sınaq Adı')
    description = models.TextField(blank=True, null=True, verbose_name='Təsvir')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma Tarixi')
    
    class Meta:
        verbose_name = 'Sınaq'
        verbose_name_plural = 'Sınaqlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class StudentResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results', verbose_name='Tələbə')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', verbose_name='Sınaq')
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Nəticə (%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma Tarixi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə Tarixi')
    
    class Meta:
        unique_together = ('student', 'exam')
        verbose_name = 'Tələbə Nəticəsi'
        verbose_name_plural = 'Tələbə Nəticələri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.exam.name}: {self.result}%"


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