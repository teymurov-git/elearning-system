from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from datetime import datetime
from .models import User, Group, MonthlyPayment


class MonthlyPaymentInline(admin.TabularInline):
    model = MonthlyPayment
    extra = 0
    can_delete = False
    fields = ('month', 'year', 'is_paid')
    readonly_fields = ('month', 'year')
    verbose_name = 'Aylıq Ödəniş'
    verbose_name_plural = 'Aylıq Ödənişlər (12 ay)'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        current_year = datetime.now().year
        return qs.filter(year=current_year).order_by('month')
    
    def has_add_permission(self, request, obj=None):
        return False


class UserAdminCustom(BaseUserAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'group', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('group', 'is_staff', 'is_superuser', 'is_active')
    inlines = [MonthlyPaymentInline]
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
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Yeni istifadəçi yaradılanda 12 ay üçün ödəniş qeydləri yarat
        if not change:  # Yalnız yeni istifadəçi üçün
            current_year = datetime.now().year
            for month in range(1, 13):
                MonthlyPayment.objects.get_or_create(
                    user=obj,
                    month=month,
                    year=current_year,
                    defaults={'is_paid': False}
                )
    
    def get_inline_instances(self, request, obj=None):
        # Mövcud istifadəçi üçün cari il üçün 12 ayın qeydlərini yoxla və yarat
        if obj and obj.pk:
            current_year = datetime.now().year
            # Yalnız yoxdursa yarat, mövcud qeydləri dəyişdirmə
            for month in range(1, 13):
                MonthlyPayment.objects.get_or_create(
                    user=obj,
                    month=month,
                    year=current_year,
                    defaults={'is_paid': False}
                )
        return super().get_inline_instances(request, obj)
    
    def save_formset(self, request, form, formset, change):
        # Django admin artıq yalnız dəyişdirilmiş qeydləri save edir
        # Amma biz əmin olmaq üçün əlavə yoxlama edirik
        if formset.model == MonthlyPayment:
            # Yalnız dəyişdirilmiş qeydləri save et
            instances = formset.save(commit=False)
            for instance in instances:
                # Hər bir qeydi ayrı-ayrılıqda save et
                instance.save()
            # Silinməsi lazım olan qeydləri sil
            for obj in formset.deleted_objects:
                obj.delete()
            formset.save_m2m()
        else:
            # Digər formset-lər üçün standart save
            super().save_formset(request, form, formset, change)


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


class MonthlyPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'year', 'is_paid', 'month_name')
    list_filter = ('is_paid', 'month', 'year', 'user__group')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_editable = ('is_paid',)
    
    def month_name(self, obj):
        return dict(MonthlyPayment.MONTH_CHOICES)[obj.month]
    month_name.short_description = 'Ay'


admin.site.register(User, UserAdminCustom)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthlyPayment, MonthlyPaymentAdmin)