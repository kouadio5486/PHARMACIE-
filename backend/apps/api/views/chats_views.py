"""
API chat — échanges patient ↔ pharmacien.
"""

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.chats.models import Chat

from ..serializers.chats_serializers import (
    ChatCreateSerializer,
    ChatSerializer,
)


class ChatViewSet(viewsets.ModelViewSet):
    """
    Permissions :
    - patient ↔ pharmacien uniquement
    - utilisateur connecté obligatoire

    Fonctionnalités :
    - envoyer un message
    - consulter ses conversations
    - consulter l'historique des échanges
    """

    queryset = Chat.objects.select_related(
        "sender",
        "receiver",
    )

    filterset_fields = (
        "sender",
        "receiver",
    )

    ordering_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

    http_method_names = [
        "get",
        "post",
        "head",
        "options",
    ]

    # ============================
    # CHOIX DU SERIALIZER
    # ============================
    def get_serializer_class(self):

        # Création d'un message
        if self.action == "create":
            return ChatCreateSerializer

        # Liste / détail
        return ChatSerializer

    # ============================
    # PERMISSIONS
    # ============================
    def get_permissions(self):
        return [IsAuthenticated()]

    # ============================
    # FILTRAGE DES MESSAGES
    # ============================
    def get_queryset(self):

        user = self.request.user

        return (
            Chat.objects.filter(
                Q(sender=user) | Q(receiver=user)
            )
            .select_related(
                "sender",
                "receiver",
            )
            .distinct()
        )

    # ============================
    # ENVOI MESSAGE
    # ============================
    def perform_create(self, serializer):

        # Le sender est automatiquement
        # l'utilisateur connecté
        serializer.save(
            sender=self.request.user
        )