from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """Custom user model dengan kolom tambahan."""
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    timezone = models.CharField(max_length=50, default="Asia/Jakarta")
    base_currency = models.CharField(max_length=3, default="IDR")
    is_onboarded = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email


class Team(TimeStampedModel):
    """Workspace bersama untuk finance tracking keluarga/tim."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_teams"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "accounts_team"

    def __str__(self) -> str:
        return self.name


class TeamMembership(TimeStampedModel):
    ROLE_VIEWER = "viewer"
    ROLE_EDITOR = "editor"
    ROLE_ADMIN = "admin"
    ROLES = [
        (ROLE_VIEWER, "Viewer"),
        (ROLE_EDITOR, "Editor"),
        (ROLE_ADMIN, "Admin"),
    ]

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_team_membership"
        unique_together = [("team", "user")]

    def __str__(self) -> str:
        return f"{self.user.email} in {self.team.name} ({self.role})"