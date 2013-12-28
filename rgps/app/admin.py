from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from rgps.app.models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    list_display = ('username', 'is_staff', 'is_superuser', 'registration_id')
    list_filter = ('is_staff', 'is_superuser')


admin.site.register(User, MyUserAdmin)