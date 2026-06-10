"""API assistant IA (optionnel)."""
# Permet de créer automatiquement les opérations CRUD
# (Create, Read, Update, Delete)
from rest_framework import viewsets
# Permission : utilisateur connecté obligatoire
from rest_framework.permissions import IsAuthenticated
# Modèle contenant les interactions IA
from apps.ai.models import AIInteraction

# IsOwnerOrAdmin : seul le propriétaire ou l'admin peut voir l'objet
# _is_admin : fonction qui vérifie si l'utilisateur est admin
from ..permissions import IsOwnerOrAdmin, _is_admin
# Serializers utilisés
from ..serializers.ai_serializers import (
    AIInteractionCreateSerializer,
    AIInteractionSerializer,
)


class AIInteractionViewSet(viewsets.ModelViewSet):
    """
    Historique des interactions IA par utilisateur.
    Types : search, symptom, general
    """
# /api/ai/?type=symptom
    filterset_fields = ("type",)
    ordering_fields = ("created_at",)
    http_method_names = ["get", "post", "head", "options"]
# Choix du serializer selon l'action
    def get_serializer_class(self):
        if self.action == "create":
            return AIInteractionCreateSerializer
        return AIInteractionSerializer

    def get_permissions(self):
        if self.action == "create":
            # Il suffit d'être connecté
            return [IsAuthenticated()]
            # connecté + propriétaire ou admin
        return [IsAuthenticated(), IsOwnerOrAdmin()]
 # Détermine quelles données l'utilisateur peut voir
    def get_queryset(self):
        # Utilisateur connecté
        user = self.request.user
        if _is_admin(user):
             # Il voit toutes les interactions
            return AIInteraction.objects.select_related("user").all()
             # l'utilisateur ne voit que ses propres interactions
        return AIInteraction.objects.filter(user=user)
 # Exécuté automatiquement lors du POST
    def perform_create(self, serializer):
        # l'interaction à l'utilisateur connecté
        serializer.save(user=self.request.user)
