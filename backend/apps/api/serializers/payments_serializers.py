from rest_framework import serializers

from apps.payments.models import Payment
from apps.deliveries.models import Delivery
from apps.reservations.models import Reservation


class PaymentSerializer(serializers.ModelSerializer):
    """
    Détails d'un paiement :
    - Medicaments → l'argent va à LA PHARMACIE,
    - Livraison    → l'argent va AU LIVREUR.
    """
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)
    methode_display = serializers.CharField(source="get_methode_display", read_only=True)
    type_paiement_display = serializers.CharField(
        source="get_type_paiement_display", read_only=True
    )
    reservation_id = serializers.IntegerField(
        source="reservation.id", read_only=True, allow_null=True
    )
    delivery_id = serializers.IntegerField(
        source="delivery.id", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "type_paiement",
            "type_paiement_display",
            "reservation",
            "reservation_id",
            "delivery",
            "delivery_id",
            "montant",
            "methode",
            "methode_display",
            "statut",
            "statut_display",
            "reference_mobile_money",
            "commentaire",
            "created_at",
            "paid_at",
        )
        read_only_fields = (
            "id", "created_at", "paid_at",
            "statut_display", "methode_display", "type_paiement_display",
            "reservation_id", "delivery_id",
        )


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Création d'un paiement :
    - type_paiement = "medicaments" : reservation_id requis (le patient paie la pharmacie)
    - type_paiement = "livraison"   : delivery_id requis (le client paie le livreur)
    """

    class Meta:
        model = Payment
        fields = (
            "type_paiement",
            "reservation",
            "delivery",
            "montant",
            "methode",
            "reference_mobile_money",
            "commentaire",
        )

    def validate_reservation(self, value):
        if not value:
            return value
        user = self.context["request"].user
        if value.user != user and not _is_admin_or_pharmacien(user, value.pharmacie):
            raise serializers.ValidationError(
                "Vous ne pouvez payer que vos propres réservations."
            )
        if value.statut not in (
            Reservation.STATUS_PENDING,
            Reservation.STATUS_CONFIRMED,
        ):
            raise serializers.ValidationError(
                "Cette réservation n'est pas éligible au paiement."
            )
        return value

    def validate_delivery(self, value):
        if not value:
            return value
        user = self.context["request"].user
        is_livreur = value.livreur == user
        is_client = value.reservation.user == user
        is_admin = _is_admin_user(user)
        if not (is_livreur or is_client or is_admin):
            raise serializers.ValidationError(
                "Vous ne pouvez pas payer cette livraison."
            )
        if value.statut_paiement_livraison == Delivery.PAIEMENT_PAYE:
            raise serializers.ValidationError(
                "Cette livraison est déjà payée."
            )
        return value

    def validate(self, attrs):
        type_paiement = attrs.get("type_paiement", Payment.TYPE_MEDICAMENTS)

        if type_paiement == Payment.TYPE_MEDICAMENTS:
            reservation = attrs.get("reservation")
            if not reservation:
                raise serializers.ValidationError(
                    {"reservation": "Une réservation est requise pour un paiement de médicaments."}
                )
            attendu = reservation.total_prix
            if attrs.get("montant") != attendu:
                raise serializers.ValidationError(
                    {"montant": f"Montant médicaments attendu : {attendu} FCFA."}
                )
        elif type_paiement == Payment.TYPE_LIVRAISON:
            delivery = attrs.get("delivery")
            if not delivery:
                raise serializers.ValidationError(
                    {"delivery": "Une livraison est requise pour un paiement de livraison."}
                )
            attendu = delivery.montant_livraison
            if attrs.get("montant") != attendu:
                raise serializers.ValidationError(
                    {"montant": f"Montant livraison attendu : {attendu} FCFA."}
                )
        return attrs


def _is_admin_or_pharmacien(user, pharmacie):
    from apps.api.permissions import _is_admin, _is_pharmacien
    if _is_admin(user):
        return True
    if _is_pharmacien(user) and pharmacie.responsable == user:
        return True
    return False


def _is_admin_user(user):
    from apps.api.permissions import _is_admin
    return _is_admin(user)
