from rest_framework import serializers
from apps.deliveries.models import Delivery
from .reservations_serializers import ReservationSerializer
from .users_serializers import UserPublicSerializer


class DeliverySerializer(serializers.ModelSerializer):
    """
    Détails complets d'une livraison : informations client,
    prix de la livraison à payer au livreur, suivi GPS,
    et statut du paiement.
    """
    reservation = ReservationSerializer(read_only=True)
    livreur = UserPublicSerializer(read_only=True)
    reservation_id = serializers.IntegerField(source="reservation.id", read_only=True)
    livreur_id = serializers.IntegerField(source="livreur.id", read_only=True)

    statut_display = serializers.CharField(source="get_statut_display", read_only=True)
    methode_paiement_livraison_display = serializers.CharField(
        source="get_methode_paiement_livraison_display", read_only=True
    )
    statut_paiement_livraison_display = serializers.CharField(
        source="get_statut_paiement_livraison_display", read_only=True
    )

    class Meta:
        model = Delivery
        fields = (
            "id",
            "reservation",
            "reservation_id",
            "livreur",
            "livreur_id",
            "montant_livraison",
            "adresse_livraison",
            "contact_client",
            "latitude",
            "longitude",
            "statut",
            "statut_display",
            "methode_paiement_livraison",
            "methode_paiement_livraison_display",
            "statut_paiement_livraison",
            "statut_paiement_livraison_display",
            "created_at",
            "livree_a",
        )
        read_only_fields = (
            "id", "created_at", "livree_a",
            "statut_display", "methode_paiement_livraison_display",
            "statut_paiement_livraison_display",
        )


class DeliveryCreateSerializer(serializers.ModelSerializer):
    """
    Création d'une livraison par LA PHARMACIE.
    Reçoit : la réservation (qui a besoin_livraison=True), un livreur,
    le montant, l'adresse et la méthode de paiement de la livraison.
    """

    class Meta:
        model = Delivery
        fields = (
            "reservation",
            "livreur",
            "montant_livraison",
            "adresse_livraison",
            "contact_client",
            "methode_paiement_livraison",
        )

    def validate_livreur(self, value):
        if value.role != "livreur":
            raise serializers.ValidationError("L'utilisateur doit être un livreur.")
        return value

    def validate_reservation(self, value):
        if not value.besoin_livraison:
            raise serializers.ValidationError(
                "Cette réservation n'a pas demandé de livraison."
            )
        if not value.paiement_medicaments_ok and value.statut not in (
            value.STATUS_CONFIRMED, value.STATUS_DONE, value.STATUS_PENDING
        ):
            # On autorise même sans paiement, en indiquant à la pharmacie de vérifier
            pass
        if value.deliveries.filter(
            statut__in=[Delivery.STATUS_EN_COURS, Delivery.STATUS_LIVRE]
        ).exists():
            raise serializers.ValidationError(
                "Une livraison est déjà en cours pour cette réservation."
            )
        return value

    def validate(self, attrs):
        montant = attrs.get("montant_livraison")
        if montant is None or montant < 0:
            raise serializers.ValidationError(
                {"montant_livraison": "Le montant de la livraison doit être ≥ 0 FCFA."}
            )
        if not attrs.get("adresse_livraison") and not attrs.get("reservation").adresse_livraison:
            raise serializers.ValidationError(
                {"adresse_livraison": "L'adresse de livraison est requise."}
            )
        return attrs

    def create(self, validated_data):
        """Si adresse non fournie, récupère celle de la réservation."""
        if not validated_data.get("adresse_livraison"):
            validated_data["adresse_livraison"] = validated_data["reservation"].adresse_livraison
        if not validated_data.get("contact_client"):
            reservation = validated_data["reservation"]
            if reservation.contact_livraison:
                validated_data["contact_client"] = reservation.contact_livraison
            else:
                validated_data["contact_client"] = reservation.user.telephone
        return super().create(validated_data)


class DeliveryGpsUpdateSerializer(serializers.ModelSerializer):
    """
    Mise à jour par le livreur : position GPS et passage en "Livré".
    Quand statut = "livre", on passe aussi statut_paiement_livraison à "paye"
    sauf si explicitement refusé.
    """

    class Meta:
        model = Delivery
        fields = (
            "latitude",
            "longitude",
            "statut",
            "statut_paiement_livraison",
            "methode_paiement_livraison",
        )

    def validate_statut(self, value):
        autorisés = {
            Delivery.STATUS_EN_COURS,
            Delivery.STATUS_LIVRE,
            Delivery.STATUS_ANNULE,
        }
        if value not in autorisés:
            raise serializers.ValidationError("Statut de livraison invalide.")
        return value

    def update(self, instance, validated_data):
        from django.utils import timezone
        if (
            validated_data.get("statut") == Delivery.STATUS_LIVRE
            and not instance.livree_a
        ):
            instance.livree_a = timezone.now()
            if (
                validated_data.get("statut_paiement_livraison")
                == Delivery.PAIEMENT_EN_ATTENTE
                or not validated_data.get("statut_paiement_livraison")
            ):
                validated_data.setdefault(
                    "statut_paiement_livraison", Delivery.PAIEMENT_PAYE
                )
        return super().update(instance, validated_data)
