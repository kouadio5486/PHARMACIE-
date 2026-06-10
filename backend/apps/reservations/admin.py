from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "pharmacie",
        "medicament",
        "quantite",
        "statut",
        "total_prix_display",
        "created_at",
    )

    list_filter = (
        "statut",
        "pharmacie",
        "created_at",
    )

    search_fields = (
        "user__nom",
        "user__prenom",
        "user__email",
        "pharmacie__nom",
        "medicament__nom",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "total_prix_display",
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
            "Détails de la réservation",
            {
                "fields": (
                    "pharmacie",
                    "medicament",
                    "quantite",
                ),
            },
        ),
        (
            "Statut",
            {
                "fields": (
                    "statut",
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
        (
            "Total",
            {
                "fields": (
                    "total_prix_display",
                ),
            },
        ),
    )

    # ==========================
    #  AFFICHAGE DU TOTAL
    # ==========================
    def total_prix_display(self, obj):
        return obj.total_prix

    total_prix_display.short_description = "Prix total (FCFA)"