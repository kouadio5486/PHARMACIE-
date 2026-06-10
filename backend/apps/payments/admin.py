from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reservation",
        "montant",
        "methode",
        "statut",
        "created_at",
    )

    list_filter = (
        "methode",
        "statut",
        "created_at",
    )

    search_fields = (
        "reservation__id",
        "reservation__user__nom",
        "reservation__user__prenom",
        "reservation__user__email",
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
            "Informations du paiement",
            {
                "fields": (
                    "reservation",
                    "montant",
                    "methode",
                ),
            },
        ),
        (
            "Statut du paiement",
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
    )