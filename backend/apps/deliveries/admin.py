from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reservation",
        "livreur",
        "montant_livraison",
        "statut",
        "statut_paiement",
        "methode_paiement",
        "position",
        "created_at",
        "livree_a",
    )

    list_filter = (
        "statut",
        "statut_paiement_livraison",
        "methode_paiement_livraison",
        "livreur",
        "created_at",
    )

    search_fields = (
        "reservation__id",
        "reservation__user__nom",
        "reservation__user__prenom",
        "livreur__nom",
        "livreur__prenom",
        "livreur__email",
        "adresse_livraison",
        "contact_client",
    )

    ordering = ("-created_at",)
    list_per_page = 30

    readonly_fields = (
        "created_at",
        "livree_a",
    )

    fieldsets = (
        (
            "Réservation & acteurs",
            {
                "fields": (
                    "reservation",
                    "livreur",
                ),
            },
        ),
        (
            "Paiement de la livraison (par le client au livreur)",
            {
                "fields": (
                    "montant_livraison",
                    "methode_paiement_livraison",
                    "statut_paiement_livraison",
                ),
                "description": (
                    "Le client paie ce montant au livreur, soit en cash, soit en Orange Money / MTN / Wave. "
                    "L'argent revient directement au livreur (pas à la pharmacie)."
                ),
            },
        ),
        (
            "Destination",
            {
                "fields": (
                    "adresse_livraison",
                    "contact_client",
                ),
            },
        ),
        (
            "Suivi GPS (livreur)",
            {
                "fields": (
                    "latitude",
                    "longitude",
                ),
            },
        ),
        (
            "Statut de livraison",
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
                    "livree_a",
                ),
            },
        ),
    )

    def position(self, obj):
        if obj.latitude and obj.longitude:
            return f" {obj.latitude}, {obj.longitude}"
        return "Aucune position"

    position.short_description = "Position GPS"

    def statut_paiement(self, obj):
        return obj.get_statut_paiement_livraison_display()

    statut_paiement.short_description = "Statut paiement livraison"

    def methode_paiement(self, obj):
        return obj.get_methode_paiement_livraison_display()

    methode_paiement.short_description = "Méthode paiement livraison"
