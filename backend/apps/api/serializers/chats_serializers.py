# Sert à transformer les objets Django (Chat) en JSON et inversement
from rest_framework import serializers

# Importe le modèle Chat (table des messages)
from apps.chats.models import Chat

# Importe le modèle User pour accéder aux rôles
from apps.users.models import User

# Serializer utilisateur public (affichage sécurisé des users)
from .users_serializers import UserPublicSerializer


# =========================================
# SERIALIZER : AFFICHAGE DES MESSAGES
# =========================================
class ChatSerializer(serializers.ModelSerializer):
    """
    Utilisé pour afficher les messages (GET)
    """

    # Infos de l'expéditeur (lecture seule)
    sender = UserPublicSerializer(read_only=True)

    # Infos du destinataire (lecture seule)
    receiver = UserPublicSerializer(read_only=True)

    class Meta:
        model = Chat

        # Champs envoyés au frontend
        fields = (
            "id",
            "sender",
            "receiver",
            "message",
            "created_at",
        )

        # Champs protégés (non modifiables via API)
        read_only_fields = (
            "id",
            "sender",
            "created_at",
        )


# =========================================
# SERIALIZER : CRÉATION DE MESSAGE
# =========================================
class ChatCreateSerializer(serializers.ModelSerializer):
    """
    Utilisé pour envoyer un message (POST)
    """

    class Meta:
        model = Chat

        fields = (
            "receiver",
            "message",
        )

    # =====================================
    # VALIDATION DU DESTINATAIRE
    # =====================================
    def validate_receiver(self, value):

        sender = self.context["request"].user

        # Empêche de s'envoyer un message à soi-même
        if sender == value:
            raise serializers.ValidationError(
                "Vous ne pouvez pas vous envoyer un message."
            )

        # Vérifie les rôles autorisés
        roles = {sender.role, value.role}

        if roles != {User.ROLE_PATIENT, User.ROLE_PHARMACIEN}:
            raise serializers.ValidationError(
                "Le chat est réservé aux échanges patient ↔ pharmacien."
            )

        return value

    # =====================================
    # VALIDATION DU MESSAGE
    # =====================================
    def validate_message(self, value):

        # Nettoyage du texte
        value = value.strip()

        # Message vide interdit
        if not value:
            raise serializers.ValidationError(
                "Le message ne peut pas être vide."
            )

        return value