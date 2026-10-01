"""API ordonnances — upload patient, validation pharmacien.

Workflow métier :
1. Patient compare les prix d'un médicament → choisit une pharmacie
2. Patient dépose son ordonnance auprès de CETTE pharmacie (pharmacie_id OBLIGATOIRE)
3. Le pharmacien de cette pharmacie voit l'ordonnance → valide ou refuse
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.ordonnances.models import Ordonnance

from ..permissions import (
    IsPatient,
    IsPharmacien,
    _is_admin,
    _is_pharmacien,
    _pharmacies_ids_of_pharmacien,
    IsPharmacienOfOrdonnanceOrAdmin,
)
from ..serializers.ordonnances_serializers import (
    OrdonnanceSerializer,
    OrdonnanceUploadSerializer,
    OrdonnanceValidationSerializer,
)


class OrdonnanceViewSet(viewsets.ModelViewSet):
    queryset = Ordonnance.objects.select_related("user", "pharmacie", "pharmacie__ville")
    filterset_fields = ("statut", "pharmacie")
    search_fields = ("user__email", "user__nom", "pharmacie__nom")
    ordering_fields = ("created_at", "statut", "updated_at")
    http_method_names = ["get", "post", "head", "options", "patch", "put"]

    def get_serializer_class(self):
        if self.action == "create":
            return OrdonnanceUploadSerializer
        if self.action in ("update", "partial_update"):
            return OrdonnanceValidationSerializer
        return OrdonnanceSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]
        if self.action in ("update", "partial_update"):
            return [IsPharmacienOfOrdonnanceOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if _is_admin(user):
            return qs
        if _is_pharmacien(user):
            pharma_ids = _pharmacies_ids_of_pharmacien(user)
            return qs.filter(pharmacie_id__in=pharma_ids)
        return qs.filter(user=user)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
