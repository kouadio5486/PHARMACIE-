from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "type",
        "is_read",
        "message_court",
        "created_at",
    )

    list_filter = (
        "type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "user__nom",
        "user__prenom",
        "user__email",
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
            "Destinataire",
            {
                "fields": (
                    "user",
                ),
            },
        ),
        (
            "Notification",
            {
                "fields": (
                    "type",
                    "message",
                    "is_read",
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