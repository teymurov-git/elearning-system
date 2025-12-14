from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import User, Group


class UserAdminCustom(BaseUserAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'group', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('group', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'group')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'group'),
        }),
    )


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count_link')
    search_fields = ('name',)
    
    def user_count_link(self, obj):
        count = obj.users.count()
        if count > 0:
            url = reverse('admin:account_user_changelist') + f'?group__id__exact={obj.id}'
            return format_html('<a href="{}">{} istifadəçi</a>', url, count)
        return '0 istifadəçi'
    user_count_link.short_description = 'İstifadəçilər'


admin.site.register(User, UserAdminCustom)
admin.site.register(Group, GroupAdmin)