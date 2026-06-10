from django.contrib import admin
from .models import AIInteraction


@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "type",
        "short_input",
        "short_output",
        "created_at",
    )

    list_filter = (
        "type",
        "created_at",
        "user",
    )

    search_fields = (
        "input",
        "output",
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
            "Utilisateur",
            {
                "fields": (
                    "user",
                    "type",
                ),
            },
        ),
        (
            "Question IA",
            {
                "fields": (
                    "input",
                ),
            },
        ),
        (
            "Réponse IA",
            {
                "fields": (
                    "output",
                ),
            },
        ),
        (
            "Contexte système",
            {
                "fields": (
                    "context",
                ),
            },
        ),
        (
            "Système",
            {
                "fields": (
                    "created_at",
                ),
            },
        ),
    )

    # =========================
    # AMÉLIORATION AFFICHAGE
    # =========================

    @admin.display(description="Entrée")
    def short_input(self, obj):
        return obj.input[:40] + "..." if len(obj.input) > 40 else obj.input

    @admin.display(description="Réponse")
    def short_output(self, obj):
        return obj.output[:40] + "..." if len(obj.output) > 40 else obj.output