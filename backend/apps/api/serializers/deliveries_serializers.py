from rest_framework import serializers
# Import du modèle Delivery (table des livraisons)
from apps.deliveries.models import Delivery
# Serializer pour afficher les détails complets d'une réservation
from .reservations_serializers import ReservationSerializer
# Serializer pour afficher les infos publiques d'un utilisateur (livreur)
from .users_serializers import UserPublicSerializer

# Serializer pour afficher les détails complets d'une livraison
class DeliverySerializer(serializers.ModelSerializer):
     # Affiche la réservation complète au lieu de juste son ID
    reservation = ReservationSerializer(read_only=True)
     # Affiche les infos du livreur (nom, prénom, etc.)
    livreur = UserPublicSerializer(read_only=True)
    # get_statut_display() est généré automatiquement par Django
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)

    class Meta:
        model = Delivery
        fields = (
            "id",
            "reservation",
            "livreur",
            "latitude",
            "longitude",
            "statut",
            "statut_display",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "statut_display")


class DeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ("reservation", "livreur")

    def validate_livreur(self, value):
        # Vérifie si l'utilisateur sélectionné est bien un livreur
        if value.role != "livreur":
             # Si ce n'est pas un livreur → erreur
            raise serializers.ValidationError("L'utilisateur doit être un livreur.")
             # Si c'est OK → on accepte
        return value

    # ==============================
    # VALIDATION GLOBALE (AMÉLIORATION)
    # ==============================
    def validate(self, attrs):

        # Récupère l'utilisateur connecté (sender)
        sender = self.context["request"].user

        # Récupère le livreur envoyé
        livreur = attrs.get("livreur")

        # Règle de sécurité :
        # seul un admin ou système peut assigner une livraison
        # (tu peux adapter selon ton projet)
        if livreur and livreur.role != "livreur":
            raise serializers.ValidationError(
                "Le livreur sélectionné n'est pas valide."
            )

        return attrs


class DeliveryGpsUpdateSerializer(serializers.ModelSerializer):
    """Mise à jour position GPS par le livreur."""

    class Meta:
        model = Delivery
        fields = ("latitude", "longitude", "statut")

    def validate_statut(self, value):
        # Liste des statuts autorisés
        autorisés = {
            Delivery.STATUS_EN_COURS,
            Delivery.STATUS_LIVRE,
            Delivery.STATUS_ANNULE,
        }
         # Vérifie si le statut envoyé est valide
        if value not in autorisés:
            raise serializers.ValidationError("Statut de livraison invalide.")
        return value
