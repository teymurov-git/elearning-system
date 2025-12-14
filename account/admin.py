from django.contrib import admin
from .models import User, UserAdmin, Group


admin.site.register(User, UserAdmin)
admin.site.register(Group)