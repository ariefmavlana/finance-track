from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team, TeamMembership

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "is_onboarded", "base_currency", "created_at"]
    search_fields = ["email", "username"]
    list_filter = ["is_onboarded", "base_currency"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Fintrack", {"fields": ("avatar", "timezone", "base_currency", "is_onboarded")}),
    )
    
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "slug", "created_at"]
    search_fields = ["name", "slug"]
    list_filter = ["owner"]


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ["team", "user", "role", "joined_at"]
    list_filter = ["role"]