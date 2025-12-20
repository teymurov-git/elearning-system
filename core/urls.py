from django.urls import path
from .views import home, check_result

urlpatterns = [
    path('', home, name='home'),
    path('netice/', check_result, name='check_result'),
]
