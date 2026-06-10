from rest_framework import serializers
# Modèle Ordonnance (table des ordonnances en base)
from apps.ordonnances.models import Ordonnance

# Serializer utilisateur (affichage sécurisé)
from .users_serializers import UserPublicSerializer


class OrdonnanceSerializer(serializers.ModelSerializer):
    """
    Serializer de lecture :
    utilisé pour afficher les ordonnances
    """

    # Affiche les infos publiques du patient
    user = UserPublicSerializer(read_only=True)

    # Affiche le label humain du statut (ex: "Validée")
    statut_display = serializers.CharField(
        source="get_statut_display",
        read_only=True
    )

    class Meta:
        model = Ordonnance
        fields = (
            "id",
            "user",
            "fichier",
            "statut",
            "statut_display",
            "commentaire",
            "created_at",
        )

        # champs non modifiables depuis l'API
        read_only_fields = ("id", "user", "created_at", "statut_display")


class OrdonnanceUploadSerializer(serializers.ModelSerializer):
    """
    Upload d'une ordonnance par un patient
    """

    class Meta:
        model = Ordonnance
        fields = ("fichier",)

    def create(self, validated_data):
        # on force le user connecté
        return Ordonnance.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )


class OrdonnanceValidationSerializer(serializers.ModelSerializer):
    """
    Validation ou refus par le pharmacien
    """

    class Meta:
        model = Ordonnance
        fields = ("statut", "commentaire")

    # ============================
    # 🔴 CORRECTION IMPORTANTE
    # ============================
    def validate(self, attrs):
        obj = self.instance

        # ❌ Empêche modification si déjà validée
        if obj and obj.statut == Ordonnance.STATUT_VALIDEE:
            raise serializers.ValidationError(
                "Impossible de modifier une ordonnance déjà validée."
            )

        return attrs

    def validate_statut(self, value):
        # Statuts autorisés pour validation pharmacien
        autorises = {
            Ordonnance.STATUT_VALIDEE,
            Ordonnance.STATUT_REFUSEE
        }

        if value not in autorises:
            raise serializers.ValidationError(
                "Le statut doit être validé ou refusé."
            )

        return value