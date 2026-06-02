"""Permission catalogue and the role → permission matrix (RBAC).

``superuser`` implicitly holds every permission (see ``User.has_permission``);
the matrix below is what gets seeded into ``role_permissions`` for the other
roles. Account management and premium toggling are intentionally superuser-only.
"""
from ssmarttv.domains.auth.models import (
    ROLE_ADMIN,
    ROLE_STAFF,
    ROLE_SUPERUSER,
    ROLE_USER,
)

# Resource:action permission slugs.
CATALOG_WRITE = "catalog:write"      # create/update movies, series, taxonomy
CATALOG_DELETE = "catalog:delete"
CHANNEL_WRITE = "channel:write"      # create/update channels
CHANNEL_DELETE = "channel:delete"
COMMENT_MODERATE = "comment:moderate"
ACCOUNT_MANAGE = "account:manage"    # create/delete staff & admin (superuser)
USER_SET_PREMIUM = "user:set_premium"  # toggle premium (superuser)

ALL_PERMISSIONS: dict[str, str] = {
    CATALOG_WRITE: "Create and update catalog content and taxonomy",
    CATALOG_DELETE: "Delete catalog content",
    CHANNEL_WRITE: "Create and update channels",
    CHANNEL_DELETE: "Delete channels",
    COMMENT_MODERATE: "Moderate user comments",
    ACCOUNT_MANAGE: "Create and delete staff/admin accounts",
    USER_SET_PREMIUM: "Grant or revoke a user's premium status",
}

# Permissions seeded per role. superuser gets everything implicitly.
ROLE_PERMISSIONS: dict[str, set[str]] = {
    ROLE_USER: set(),
    ROLE_STAFF: {CATALOG_WRITE, CHANNEL_WRITE},
    ROLE_ADMIN: {
        CATALOG_WRITE,
        CATALOG_DELETE,
        CHANNEL_WRITE,
        CHANNEL_DELETE,
        COMMENT_MODERATE,
    },
    ROLE_SUPERUSER: set(ALL_PERMISSIONS),
}

ROLE_NAMES: dict[str, str] = {
    ROLE_USER: "User",
    ROLE_STAFF: "Staff",
    ROLE_ADMIN: "Administrator",
    ROLE_SUPERUSER: "Superuser",
}
