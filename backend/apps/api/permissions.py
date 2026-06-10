from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.models import User


def _role(user):
    return getattr(user, "role", None)


def _is_admin(user):
    return user.is_authenticated and (
        _role(user) == User.ROLE_ADMIN or user.is_superuser
    )


def _is_pharmacien(user):
    return user.is_authenticated and _role(user) == User.ROLE_PHARMACIEN


def _is_patient(user):
    return user.is_authenticated and _role(user) == User.ROLE_PATIENT


def _is_livreur(user):
    return user.is_authenticated and _role(user) == User.ROLE_LIVREUR


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return _is_admin(request.user)


class IsPharmacien(BasePermission):
    def has_permission(self, request, view):
        return _is_pharmacien(request.user) or _is_admin(request.user)


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return _is_patient(request.user) or _is_admin(request.user)


class IsLivreur(BasePermission):
    def has_permission(self, request, view):
        return _is_livreur(request.user) or _is_admin(request.user)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return _is_admin(request.user)


class IsOwnerOrAdmin(BasePermission):
    """Objet avec attribut user ou sender."""

    def has_object_permission(self, request, view, obj):
        if _is_admin(request.user):
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "sender", None)
        return owner == request.user
