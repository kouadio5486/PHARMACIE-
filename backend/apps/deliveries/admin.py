from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reservation",
        "livreur",
        "statut",
        "position",
        "created_at",
    )

    list_filter = (
        "statut",
        "livreur",
        "created_at",
    )

    search_fields = (
        "reservation__id",
        "livreur__nom",
        "livreur__prenom",
        "livreur__email",
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
            "Informations livraison",
            {
                "fields": (
                    "reservation",
                    "livreur",
                ),
            },
        ),
        (
            "Position GPS",
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
                ),
            },
        ),
    )

    # ==========================
    #  POSITION GPS (AMÉLIORÉ)
    # ==========================
    def position(self, obj):
        if obj.latitude and obj.longitude:
            return f" {obj.latitude}, {obj.longitude}"
        return "Aucune position"

    position.short_description = "Position GPS"