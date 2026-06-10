from django.db import models
from apps.users.models import User


class AIInteraction(models.Model):
    """
    Historique des recherches IA (assistant pharmacie).
    """

    TYPE_SEARCH = "search"
    TYPE_SYMPTOM = "symptom"
    TYPE_GENERAL = "general"

    TYPE_CHOICES = [
        (TYPE_SEARCH, "Recherche médicament"),
        (TYPE_SYMPTOM, "Recherche par symptôme"),
        (TYPE_GENERAL, "Question générale"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ai_interactions",
        verbose_name="Utilisateur"
    )

    input = models.TextField(
        verbose_name="Entrée utilisateur",
    )

    output = models.TextField(
        verbose_name="Réponse du système",
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_GENERAL,
        verbose_name="Type de recherche"
    )

    context = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Contexte de recherche"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        db_table = "ai_interactions"
        verbose_name = "Interaction IA"
        verbose_name_plural = "Interactions IA"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.input[:30]}"