from django.contrib import admin
from .models import Ordonnance


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "pharmacie",
        "statut",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "statut",
        "pharmacie",
        "pharmacie__ville",
        "created_at",
    )

    search_fields = (
        "user__nom",
        "user__prenom",
        "user__email",
        "pharmacie__nom",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Acteurs",
            {
                "fields": (
                    "user",
                    "pharmacie",
                ),
            },
        ),
        (
            "Contenu ordonnance",
            {
                "fields": (
                    "fichier",
                    "medicaments_extraits",
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
                    "updated_at",
                ),
            },
        ),
    )