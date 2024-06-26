from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "status", "role", "tag", "image")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(UserToProject)
admin.site.register(Team)
admin.site.register(UserToTeam)
admin.site.register(ProjectInvite)
admin.site.register(TeamInvite)
admin.site.register(TaskComment)
admin.site.register(Permissions)

