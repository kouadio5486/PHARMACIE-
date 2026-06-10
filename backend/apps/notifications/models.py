from django.db import models

from apps.users.models import User


class Notification(models.Model):
    """
    Notifications envoyées aux utilisateurs.
    """

    TYPE_INFO = "info"
    TYPE_ALERT = "alert"
    TYPE_SUCCESS = "success"

    TYPE_CHOICES = [
        (TYPE_INFO, "Information"),
        (TYPE_ALERT, "Alerte"),
        (TYPE_SUCCESS, "Succès"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Utilisateur",
    )

    message = models.TextField(
        verbose_name="Message",
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_INFO,
        verbose_name="Type",
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Lu",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.nom} - "
            f"{self.get_type_display()}"
        )