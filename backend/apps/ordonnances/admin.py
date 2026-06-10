from django.contrib import admin
from .models import Ordonnance


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "statut",
        "created_at",
    )

    list_filter = (
        "statut",
        "created_at",
    )

    search_fields = (
        "user__nom",
        "user__prenom",
        "user__email",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Informations utilisateur",
            {
                "fields": (
                    "user",
                ),
            },
        ),
        (
            "Fichier ordonnance",
            {
                "fields": (
                    "fichier",
                ),
            },
        ),
        (
            "Statut de validation",
            {
                "fields": (
                    "statut",
                    "commentaire",
                ),
            },
        ),
        (
            "Informations système",
            {
                "fields": (
                    "created_at",
                ),
            },
        ),
    )