from rest_framework import serializers

from apps.payments.models import Payment
# Import du modèle Payment
# Représente les paiements enregistrés dans la base.
from apps.reservations.models import Reservation


class PaymentSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)
    methode_display = serializers.CharField(source="get_methode_display", read_only=True)
    reservation_id = serializers.IntegerField(source="reservation.id", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "reservation",
            "reservation_id",
            "montant",
            "methode",
            "methode_display",
            "statut",
            "statut_display",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "statut_display", "methode_display")


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("reservation", "montant", "methode")

    def validate_reservation(self, value):
        user = self.context["request"].user
        if value.user != user:
            raise serializers.ValidationError(
                "Vous ne pouvez payer que vos propres réservations."
            )
             # Vérifie que la réservation peut être payée
        if value.statut not in (
            Reservation.STATUS_PENDING,
            Reservation.STATUS_CONFIRMED,
        ):
            raise serializers.ValidationError(
                "Cette réservation n'est pas éligible au paiement."
            )
        return value

    def validate(self, attrs):
        reservation = attrs["reservation"]
        # Montant attendu calculé dans la réservation
        attendu = reservation.total_prix
         # Vérifie que le montant envoyé
        # correspond exactement au prix attendu
        if attrs["montant"] != attendu:
            raise serializers.ValidationError(
                {"montant": f"Le montant attendu est {attendu} FCFA."}
            )
        return attrs
