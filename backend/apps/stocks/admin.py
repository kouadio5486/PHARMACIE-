from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "pharmacie",
        "medicament",
        "quantite",
        "prix",
        "seuil_alerte",
        "stock_faible",
        "date_mise_a_jour",
        "created_at",
    )

    list_filter = (
        "pharmacie",
        "medicament",
        "date_mise_a_jour",
        "created_at",
    )

    search_fields = (
        "pharmacie__nom",
        "medicament__nom",
    )

    ordering = (
        "pharmacie",
        "medicament",
    )

    list_per_page = 20

    readonly_fields = (
        "date_mise_a_jour",
        "created_at",
    )

    fieldsets = (
        (
            "Informations du stock",
            {
                "fields": (
                    "pharmacie",
                    "medicament",
                    "quantite",
                    "prix",
                    "seuil_alerte",
                ),
            },
        ),
        (
            "Système",
            {
                "fields": (
                    "date_mise_a_jour",
                    "created_at",
                ),
            },
        ),
    )