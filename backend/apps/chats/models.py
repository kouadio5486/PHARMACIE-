from django.db import models

from apps.users.models import User


class Chat(models.Model):
    """
    Messages échangés entre patients et pharmaciens.
    """

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_envoyes",
        verbose_name="Expéditeur",
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_recus",
        verbose_name="Destinataire",
    )

    message = models.TextField(
        verbose_name="Message",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi",
    )

    class Meta:
        db_table = "chats"
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.sender.nom} → "
            f"{self.receiver.nom}"
        )