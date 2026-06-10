from rest_framework import serializers
# Représente une réservation de médicament en pharmacie
from apps.reservations.models import Reservation
# Sert à vérifier la disponibilité du médicament dans une pharmacie
from apps.stocks.models import Stock
# Serializer médicament (affichage)
from .medicaments_serializers import MedicamentListSerializer
# Serializer pharmacie (affichage)
from .pharmacies_serializers import PharmacieListSerializer
# Serializer utilisateur (affichage)
from .users_serializers import UserPublicSerializer


class ReservationSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    pharmacie = PharmacieListSerializer(read_only=True)
    medicament = MedicamentListSerializer(read_only=True)
    total_prix = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "user",
            "pharmacie",
            "medicament",
            "quantite",
            "statut",
            "statut_display",
            "total_prix",
            "created_at",
        )
        read_only_fields = ("id", "user", "total_prix", "created_at", "statut_display")


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Création de réservation par le patient."""

    class Meta:
        model = Reservation
        fields = ("pharmacie", "medicament", "quantite")

    def validate(self, attrs):
        pharmacie = attrs["pharmacie"]
        medicament = attrs["medicament"]
        quantite = attrs["quantite"]
 # Vérifie que la pharmacie est active
        if not pharmacie.is_active:
            raise serializers.ValidationError(
                {"pharmacie": "Cette pharmacie n'est pas active."}
            )
 # Vérifie le stock du médicament dans cette pharmacie
        stock = Stock.objects.filter(
            pharmacie=pharmacie, medicament=medicament
        ).first()

        if not stock or stock.quantite < quantite:
            raise serializers.ValidationError(
                {"quantite": "Stock insuffisant dans cette pharmacie."}
            )
 # Vérifie si ordonnance obligatoire
        if medicament.ordonnance_requise:
             # Utilisateur connecté
            user = self.context["request"].user
            ordonnance_validee = user.ordonnances.filter(statut="validee").exists()
            if not ordonnance_validee:
                raise serializers.ValidationError(
                    "Une ordonnance validée est requise pour ce médicament."
                )

        return attrs


class ReservationStatutSerializer(serializers.ModelSerializer):
    """Validation / refus par le pharmacien."""

    class Meta:
        model = Reservation
         # Le pharmacien ne change que le statut
        fields = ("statut",)

    def validate_statut(self, value):
        # Liste des statuts autorisés
        autorisés = {
            Reservation.STATUS_CONFIRMED,
            Reservation.STATUS_CANCELLED,
            Reservation.STATUS_DONE,
        }
          # Vérifie si le statut est valide
        if value not in autorisés:
            raise serializers.ValidationError("Statut non autorisé pour cette action.")
        return value
