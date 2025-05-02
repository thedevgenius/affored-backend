from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone',)
    ordering = ('-id',)
    readonly_fields = ('profile_image', 'profile_color')
    fieldsets = (
        (None, {'fields': ('phone', 'password', 'profile_image', 'profile_color')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(User, UserAdmin)
