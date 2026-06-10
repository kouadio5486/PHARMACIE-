"""API ordonnances — upload patient, validation pharmacien."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.ordonnances.models import Ordonnance

from ..permissions import IsPatient, IsPharmacien, _is_admin, _is_pharmacien
from ..serializers.ordonnances_serializers import (
    OrdonnanceSerializer,
    OrdonnanceUploadSerializer,
    OrdonnanceValidationSerializer,
)


class OrdonnanceViewSet(viewsets.ModelViewSet):
    """
    Permissions :
    - patient → upload fichier
    - pharmacien → validation (en_attente / validee / refusee)
    Statuts : en_attente, validee, refusee
    """

    queryset = Ordonnance.objects.select_related("user")
    filterset_fields = ("statut",)
    search_fields = ("user__email", "user__nom")
    ordering_fields = ("created_at", "statut")
    http_method_names = ["get", "post", "head", "options", "patch", "put"]

    def get_serializer_class(self):
        # Patient upload une ordonnance
        if self.action == "create":
            return OrdonnanceUploadSerializer
             # Pharmacien valide ou refuse
        if self.action in ("update", "partial_update"):
            return OrdonnanceValidationSerializer
        return OrdonnanceSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]
            # seul pharmacien peut valider
        if self.action in ("update", "partial_update"):
            return [IsPharmacien()]
              # lecture pour utilisateurs connectés
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # admin et pharmacien voient tout
        if _is_admin(user) or _is_pharmacien(user):
            return qs
             # patient ne voit que ses propres ordonnances
        return qs.filter(user=user)
