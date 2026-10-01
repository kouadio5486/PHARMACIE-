from rest_framework import serializers
# Modèle Ordonnance (table des ordonnances en base)
from apps.ordonnances.models import Ordonnance
from apps.pharmacies.models import Pharmacie

# Serializer utilisateur (affichage sécurisé)
from .users_serializers import UserPublicSerializer
from .pharmacies_serializers import PharmacieListSerializer


class OrdonnanceSerializer(serializers.ModelSerializer):
    """
    Serializer de lecture :
    utilisé pour afficher les ordonnances
    """

    user = UserPublicSerializer(read_only=True)
    pharmacie = PharmacieListSerializer(read_only=True)

    statut_display = serializers.CharField(
        source="get_statut_display",
        read_only=True
    )

    class Meta:
        model = Ordonnance
        fields = (
            "id",
            "user",
            "pharmacie",
            "fichier",
            "medicaments_extraits",
            "statut",
            "statut_display",
            "commentaire",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("id", "user", "pharmacie", "created_at", "updated_at", "statut_display")


class OrdonnanceUploadSerializer(serializers.ModelSerializer):
    """
    Upload d'une ordonnance par un patient.

    Workflow :
    1. Le patient a déjà comparé les prix et choisi sa pharmacie.
    2. Il envoie pharmacie_id + fichier + (optionnel) les médicaments extraits.
    """

    pharmacie_id = serializers.PrimaryKeyRelatedField(
        queryset=Pharmacie.objects.filter(is_active=True),
        write_only=True,
        required=True,
        help_text="ID de la pharmacie choisie par le patient (souvent la moins chère).",
    )

    medicaments_extraits = serializers.JSONField(
        required=False,
        allow_null=True,
        help_text="Liste des médicaments de l'ordonnance. Format : [{nom, dosage, quantite}]",
    )

    class Meta:
        model = Ordonnance
        fields = ("fichier", "pharmacie_id", "medicaments_extraits")

    def create(self, validated_data):
        pharmacie = validated_data.pop("pharmacie_id")
        return Ordonnance.objects.create(
            user=self.context["request"].user,
            pharmacie=pharmacie,
            **validated_data,
        )


class OrdonnanceValidationSerializer(serializers.ModelSerializer):
    """
    Validation ou refus par le pharmacien
    """

    class Meta:
        model = Ordonnance
        fields = ("statut", "commentaire")

    def validate(self, attrs):
        obj = self.instance

        if obj and obj.statut == Ordonnance.STATUT_VALIDEE:
            raise serializers.ValidationError(
                "Impossible de modifier une ordonnance déjà validée."
            )

        return attrs

    def validate_statut(self, value):
        autorises = {
            Ordonnance.STATUT_VALIDEE,
            Ordonnance.STATUT_REFUSEE
        }

        if value not in autorises:
            raise serializers.ValidationError(
                "Le statut doit être validé ou refusé."
            )

        return value