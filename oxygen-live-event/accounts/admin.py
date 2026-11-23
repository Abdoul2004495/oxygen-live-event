# The admin toolkit (provides @admin.register and the admin site)
from django.contrib import admin
# Django's ready-made admin page for users, which we customize
from django.contrib.auth.admin import UserAdmin

# Import our User model from models.py in the same folder (the dot means "same folder")
from .models import User


# Registers this class as the admin page for the User model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Sort the user list by email (the default sorts by username, which no longer exists)
    ordering = ("email",)
    # Columns shown in the user list page
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    # Filter box shown on the right side of the list page
    list_filter = ("role", "is_staff", "is_active")
    # Columns the search box looks into
    search_fields = ("email", "first_name", "last_name", "phone")

    # Layout of the EDIT page: each item is (section title, {"fields": (...)})
    fieldsets = (
        # None = a section without a title
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "gender", "city", "country",)}),
        ("Role and permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Layout of the CREATE page (password typed twice: password1 and password2)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),   # makes the form wider
            "fields": ("email", "phone", "role", "password1", "password2"),
        }),
    )