from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import MyUser


class MyUserAdmin(UserAdmin):
    # UserAdmin에서 fieldsets만 가져와서 커스터마이징
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # field 커스텀
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'my_photo',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(MyUser, MyUserAdmin)