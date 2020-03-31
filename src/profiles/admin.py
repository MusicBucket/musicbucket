from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from rest_framework.authtoken.admin import TokenAdmin

from profiles.models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(OriginalUserAdmin):
    """Add profile inline to original UserAdmin class"""
    inlines = [UserProfileInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_activation_date')

    @staticmethod
    def profile_activation_date(obj):
        return obj.profile.activation_date


user_model = get_user_model()
try:
    admin.site.unregister(user_model)
finally:
    admin.site.register(user_model, UserAdmin)

# Monkey patching to have the user in the Token admin section
TokenAdmin.raw_id_fields = ['user']
