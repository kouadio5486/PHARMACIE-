from django.contrib import admin

from .models import Medicament


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nom",
        "dosage",
        "categorie",
        "laboratoire",
        "ordonnance_requise",
        "created_at",
    )

    list_filter = (
        "categorie",
        "ordonnance_requise",
        "laboratoire",
        "created_at",
    )

    search_fields = (
        "nom",
        "laboratoire",
        "categorie",
        "qr_code",
    )

    ordering = ("nom",)
    list_per_page = 20

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Informations du médicament",
            {
                "fields": (
                    "nom",
                    "dosage",
                    "description",
                    "categorie",
                    "laboratoire",
                ),
            },
        ),
        (
            "Image et authentification",
            {
                "fields": (
                    "image",
                    "qr_code",
                ),
            },
        ),
        (
            "Conditions de vente",
            {
                "fields": ("ordonnance_requise",),
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
