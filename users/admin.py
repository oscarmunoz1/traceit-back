from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WorksIn, VerificationCode
from .forms import CustomUserCreationForm, CustomUserChangeForm


class RoleInline(admin.TabularInline):
    model = WorksIn
    extra = 1


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = ["email"]
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (RoleInline,)
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = ("email", "is_staff", "is_active", "is_superuser", "user_type")
    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        (
            ("Personal info"),
            {"fields": ("first_name", "last_name", "email", "user_type")},
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "user_type",
                ),
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
admin.site.register(VerificationCode)
