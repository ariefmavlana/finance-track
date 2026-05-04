from django.core.exceptions import PermissionDenied


def assert_owns(user, obj) -> None:
    """
    Raise PermissionDenied jika user tidak memiliki object.
    Supports user FK dan team membership.
    """
    if hasattr(obj, "user") and obj.user_id != user.pk:
        raise PermissionDenied(
            f"User {user.email} does not own {obj.__class__.__name__} {obj.pk}"
        )
    if hasattr(obj, "team") and obj.team:
        if not obj.team.memberships.filter(user=user).exists():
            raise PermissionDenied(
                f"User {user.email} is not a member of team {obj.team.name}"
            )
