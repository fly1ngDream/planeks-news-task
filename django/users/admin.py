from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreateForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_superuser', 'is_active']


admin.site.register(CustomUser, CustomUserAdmin)
