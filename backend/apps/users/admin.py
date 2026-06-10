from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # Liste des utilisateurs
    list_display = (
        "id",
        "nom",
        "prenom",
        "email",
        "telephone",
        "role",
        "permissions_display",
        "is_active",
        "is_verified",
        "is_staff",
        "created_at",
    )

    # Filtres
    list_filter = (
        "role",
        "is_active",
        "is_verified",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    # Recherche
    search_fields = (
        "nom",
        "prenom",
        "email",
        "telephone",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    # Champs en lecture seule
    readonly_fields = (
        "permissions_display",
        "created_at",
        "updated_at",
        "last_login",
    )

    # Formulaire modification
    fieldsets = (
        (
            "Informations personnelles",
            {
                "classes": ("wide",),
                "fields": (
                    "nom",
                    "prenom",
                    "email",
                    "telephone",
                    "photo",
                    "adresse",
                ),
            },
        ),
        (
            "Authentification",
            {
                "classes": ("wide",),
                "fields": (
                    "password",
                    "last_login",
                ),
            },
        ),
        (
            "Rôle",
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "permissions_display",
                ),
            },
        ),
        (
            "Permissions Django",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    # Formulaire ajout utilisateur
    add_fieldsets = (
        (
            "Nouvel utilisateur",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nom",
                    "prenom",
                    "telephone",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display(description="Permissions métier")
    def permissions_display(self, obj):
        permissions = {
            "patient": [
                "recherche",
                "reservation",
                "ordonnance",
            ],
            "pharmacien": [
                "stock",
                "validation",
                "gestion_pharmacie",
            ],
            "livreur": [
                "livraison",
                "gps",
            ],
            "admin": [
                "tout",
            ],
        }

        return ", ".join(
            permissions.get(obj.role, [])
        ) or "-"