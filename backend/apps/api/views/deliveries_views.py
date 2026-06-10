from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.deliveries.models import Delivery

from ..permissions import IsLivreur, IsPharmacien, _is_admin, _is_livreur, _is_pharmacien
from ..serializers.deliveries_serializers import (
    DeliveryCreateSerializer,
    DeliveryGpsUpdateSerializer,
    DeliverySerializer,
)


class DeliveryViewSet(viewsets.ModelViewSet):
    """
    API livraisons :
    - création (pharmacien)
    - GPS (livreur)
    - lecture (selon rôle)
    """

    queryset = Delivery.objects.select_related(
        "reservation", "livreur", "reservation__pharmacie"
    )

    filterset_fields = ("statut", "livreur")
    ordering_fields = ("created_at", "statut")

    # =========================
    # SERIALIZER
    # =========================
    def get_serializer_class(self):

        if self.action == "create":
            return DeliveryCreateSerializer

        # GPS update → livreur uniquement
        if self.action in ("update", "partial_update"):
            return DeliveryGpsUpdateSerializer

        return DeliverySerializer

    # =========================
    # PERMISSIONS
    # =========================
    def get_permissions(self):

        # création → pharmacien uniquement
        if self.action == "create":
            return [IsPharmacien()]

        # update GPS → livreur uniquement
        if self.action in ("update", "partial_update"):
            return [IsLivreur()]

        # lecture → utilisateur connecté
        return [IsAuthenticated()]

    # =========================
    # FILTRAGE DES DONNÉES
    # =========================
    def get_queryset(self):

        qs = super().get_queryset()
        user = self.request.user

        # ADMIN → tout voir
        if _is_admin(user):
            return qs

        # LIVREUR → ses livraisons
        if _is_livreur(user):
            return qs.filter(livreur=user)

        # PHARMACIEN → ses pharmacies
        if _is_pharmacien(user):
            return qs.filter(reservation__pharmacie__responsable=user)

        # CLIENT → ses commandes
        return qs.filter(reservation__user=user)

    # =========================
    # CRÉATION SÉCURISÉE (IMPORTANT)
    # =========================
    def perform_create(self, serializer):

        # Ici tu sécurises encore plus :
        # le serializer valide déjà le livreur,
        # mais on peut ajouter des règles backend si besoin.

        serializer.save()