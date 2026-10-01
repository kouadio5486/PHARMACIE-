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
        "besoin_livraison",
        "paiement_ok",
        "livree",
        "total_prix_display",
        "created_at",
    )

    list_filter = (
        "statut",
        "besoin_livraison",
        "pharmacie",
        "created_at",
    )

    search_fields = (
        "user__nom",
        "user__prenom",
        "user__email",
        "pharmacie__nom",
        "medicament__nom",
        "adresse_livraison",
    )

    ordering = ("-created_at",)
    list_per_page = 30

    readonly_fields = (
        "created_at",
        "updated_at",
        "total_prix_display",
        "paiement_ok",
        "livree",
    )

    fieldsets = (
        (
            "Informations patient",
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
            "Option livraison",
            {
                "fields": (
                    "besoin_livraison",
                    "adresse_livraison",
                    "contact_livraison",
                ),
                "description": (
                    "Si besoin_livraison est coché : la pharmacie créera une Delivery. "
                    "Le patient paie les médicaments à la pharmacie, "
                    "PUIS paie la livraison (en espèces / Mobile Money) au livreur à la réception."
                ),
            },
        ),
        (
            "Statut & suivi",
            {
                "fields": (
                    "statut",
                    "paiement_ok",
                    "livree",
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
        (
            "Total médicaments (sans livraison)",
            {
                "fields": (
                    "total_prix_display",
                ),
            },
        ),
    )

    def total_prix_display(self, obj):
        return f"{obj.total_prix} FCFA"

    total_prix_display.short_description = "Prix médicaments (FCFA)"

    def paiement_ok(self, obj):
        return obj.paiement_medicaments_ok

    paiement_ok.boolean = True
    paiement_ok.short_description = "Médicaments payés"

    def livree(self, obj):
        return obj.deliveries.filter(statut=Delivery.STATUS_LIVRE).exists()

    livree.boolean = True
    livree.short_description = "Livrée"


from apps.deliveries.models import Delivery  # noqa: E402
