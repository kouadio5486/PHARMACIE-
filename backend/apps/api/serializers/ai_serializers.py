# Importe le module serializers de Django REST Framework.
# Les serializers permettent de convertir les objets Python/Django en JSON
# et inversement (JSON -> objet Django).
from rest_framework import serializers

from apps.ai.models import AIInteraction
# Importe un serializer qui permet d'afficher les informations publiques d'un utilisateur.

from .users_serializers import UserPublicSerializer

# Crée un serializer pour les interactions avec l'IA.
class AIInteractionSerializer(serializers.ModelSerializer):
    # Affiche les informations publiques d'un utilisateur.
    user = UserPublicSerializer(read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        # Définit le modèle à utiliser pour le serializer.
        model = AIInteraction
         # Liste des champs qui seront retournés dans la réponse JSON.
        fields = (
            "id",
            "user",
            "input",
            "input_audio",
            "output",
            "output_audio",
            "type",
            "type_display",
            "context",
            "created_at",
        )
         # Ils peuvent être affichés mais ne peuvent pas être modifiés
        # depuis le frontend.
        read_only_fields = ("id", "user", "created_at", "type_display")

# Cela permet plus de sécurité et de flexibilité.
class AIInteractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        # Champs autorisés lors de la création.
        model = AIInteraction
        fields = ("input", "input_audio", "output", "output_audio", "type", "context")
        # Champs qui seront utilisés pour la création.
    def create(self, validated_data):
        return AIInteraction.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )
