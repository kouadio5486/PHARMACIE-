from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sender",
        "receiver",
        "message_court",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "sender__nom",
        "sender__prenom",
        "sender__email",
        "receiver__nom",
        "receiver__prenom",
        "receiver__email",
        "message",
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
            "Participants",
            {
                "fields": (
                    "sender",
                    "receiver",
                ),
            },
        ),
        (
            "Contenu du message",
            {
                "fields": (
                    "message",
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

    def message_court(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message

    message_court.short_description = "Message"