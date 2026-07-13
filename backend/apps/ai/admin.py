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
        "has_input_audio",
        "has_output_audio",
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
                    "input_audio",
                ),
            },
        ),
        (
            "Réponse IA",
            {
                "fields": (
                    "output",
                    "output_audio",
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
        return obj.input[:40] + "..." if (obj.input and len(obj.input) > 40) else obj.input or "-"

    @admin.display(description="Réponse")
    def short_output(self, obj):
        return obj.output[:40] + "..." if (obj.output and len(obj.output) > 40) else obj.output or "-"

    @admin.display(description="Audio entrée", boolean=True)
    def has_input_audio(self, obj):
        return bool(obj.input_audio)

    @admin.display(description="Audio réponse", boolean=True)
    def has_output_audio(self, obj):
        return bool(obj.output_audio)