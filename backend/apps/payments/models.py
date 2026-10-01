from django.db import models

from apps.reservations.models import Reservation


class Payment(models.Model):
    """
    Paiements sur la plateforme :
    - TYPE : "medicaments" → payé par le client → l'argent va à LA PHARMACIE
    - TYPE : "livraison"    → payé par le client → l'argent va au LIVREUR
    """

    TYPE_MEDICAMENTS = "medicaments"
    TYPE_LIVRAISON = "livraison"

    TYPE_CHOICES = [
        (TYPE_MEDICAMENTS, "Paiement des médicaments → Pharmacie"),
        (TYPE_LIVRAISON, "Paiement de la livraison → Livreur"),
    ]

    METHODE_ORANGE_MONEY = "orange_money"
    METHODE_MTN = "mtn"
    METHODE_WAVE = "wave"
    METHODE_CARTE = "carte"
    METHODE_ESPECES = "especes"

    METHODE_CHOICES = [
        (METHODE_ORANGE_MONEY, "Orange Money"),
        (METHODE_MTN, "MTN Mobile Money"),
        (METHODE_WAVE, "Wave"),
        (METHODE_CARTE, "Carte Bancaire"),
        (METHODE_ESPECES, "Espèces (cash)"),
    ]

    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_SUCCESS, "Succès"),
        (STATUS_FAILED, "Échec"),
    ]

    type_paiement = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default=TYPE_MEDICAMENTS,
        verbose_name="Type de paiement",
        help_text="Détermine à qui revient l'argent : pharmacie (médicaments) ou livreur (livraison).",
    )

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Réservation concernée",
        null=True,
        blank=True,
        help_text="Requis pour un paiement de médicaments.",
    )

    delivery = models.ForeignKey(
        "deliveries.Delivery",
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Livraison concernée",
        null=True,
        blank=True,
        help_text="Requis pour un paiement de livraison.",
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Montant",
        help_text="Montant payé en FCFA",
    )

    methode = models.CharField(
        max_length=20,
        choices=METHODE_CHOICES,
        verbose_name="Méthode de paiement",
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Statut",
    )

    reference_mobile_money = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Référence transaction Mobile Money",
        help_text="Identifiant de la transaction renvoyé par Orange Money / MTN / Wave.",
    )

    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date d'encaissement",
    )

    class Meta:
        db_table = "payments"
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["type_paiement", "statut"]),
            models.Index(fields=["reservation"]),
            models.Index(fields=["delivery"]),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.type_paiement == self.TYPE_MEDICAMENTS and not self.reservation:
            raise ValidationError(
                {"reservation": "Une réservation est requise pour un paiement de médicaments."}
            )
        if self.type_paiement == self.TYPE_LIVRAISON and not self.delivery:
            raise ValidationError(
                {"delivery": "Une livraison est requise pour un paiement de livraison."}
            )

    def __str__(self):
        dest = "→ Pharmacie" if self.type_paiement == self.TYPE_MEDICAMENTS else "→ Livreur"
        return (
            f"Paiement #{self.id} [{self.get_type_paiement_display()}] - "
            f"{self.montant} FCFA {dest} - "
            f"{self.get_methode_display()} - {self.get_statut_display()}"
        )