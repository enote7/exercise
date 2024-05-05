from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Testimonial
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_superuser', 'email_confirmed')  # Include 'email_confirmed'
    search_fields = ('email', 'username')
    readonly_fields = ('last_login',)  # Remove 'date_joined'

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Email Confirmation', {'fields': ('email_confirmed',)}),  # Add this line for email confirmation
        ('Important dates', {'fields': ('last_login',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'email_confirmed', 'profile_picture')}  # Include email_confirmed in add fieldsets
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'created_at', 'user')
    search_fields = ('feedback',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
