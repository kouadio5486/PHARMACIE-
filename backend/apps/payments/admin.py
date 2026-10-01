from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "type_paiement",
        "reservation",
        "delivery",
        "destinataire",
        "montant",
        "methode",
        "statut",
        "created_at",
        "paid_at",
    )

    list_filter = (
        "type_paiement",
        "methode",
        "statut",
        "created_at",
        "paid_at",
    )

    search_fields = (
        "reservation__id",
        "reservation__user__nom",
        "reservation__user__prenom",
        "reservation__pharmacie__nom",
        "delivery__id",
        "delivery__livreur__nom",
        "delivery__livreur__prenom",
        "reference_mobile_money",
        "commentaire",
    )

    ordering = ("-created_at",)
    list_per_page = 30

    readonly_fields = (
        "created_at",
        "paid_at",
    )

    fieldsets = (
        (
            "Type & destinataire",
            {
                "fields": (
                    "type_paiement",
                    "reservation",
                    "delivery",
                ),
                "description": (
                    "• Medicaments : paiement du client → L'ARGENT VA À LA PHARMACIE.\n"
                    "• Livraison : paiement du client → L'ARGENT VA AU LIVREUR (cash ou mobile money)."
                ),
            },
        ),
        (
            "Montant & méthode",
            {
                "fields": (
                    "montant",
                    "methode",
                    "reference_mobile_money",
                ),
            },
        ),
        (
            "Statut",
            {
                "fields": (
                    "statut",
                    "commentaire",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "paid_at",
                ),
            },
        ),
    )

    def destinataire(self, obj):
        if obj.type_paiement == Payment.TYPE_MEDICAMENTS and obj.reservation_id:
            return f"Pharmacie : {obj.reservation.pharmacie.nom}"
        if obj.type_paiement == Payment.TYPE_LIVRAISON and obj.delivery_id:
            return f"Livreur : {obj.delivery.livreur.nom} {obj.delivery.livreur.prenom}"
        return "—"

    destinataire.short_description = "À qui l'argent ?"
