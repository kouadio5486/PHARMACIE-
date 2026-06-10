"""API réservations — commandes patient (statut CharField)."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.reservations.models import Reservation

# Permissions selon rôle utilisateur
from ..permissions import IsPatient, IsPharmacien, _is_admin, _is_pharmacien

# Serializers (différents selon action)
from ..serializers.reservations_serializers import (
    ReservationCreateSerializer,
    ReservationSerializer,
    ReservationStatutSerializer,
)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API des réservations :

     Patient → crée une réservation
     Pharmacien → valide / refuse / termine
     Admin → supervision totale

    Statuts possibles :
    - pending
    - confirmed
    - cancelled
    - done
    """

    # Optimisation SQL (évite requêtes inutiles)
    queryset = Reservation.objects.select_related(
        "user", "pharmacie", "medicament"
    )

    # filtres automatiques API
    filterset_fields = ("statut", "pharmacie", "medicament")
    search_fields = ("user__email", "medicament__nom", "pharmacie__nom")
    ordering_fields = ("created_at", "statut")

    # =========================
    # SERIALIZER SELON ACTION
    # =========================
    def get_serializer_class(self):

        # création réservation (patient)
        if self.action == "create":
            return ReservationCreateSerializer

        # update statut (pharmacien)
        if self.action in ("update", "partial_update"):
            return ReservationStatutSerializer

        # lecture
        return ReservationSerializer

    # =========================
    # PERMISSIONS
    # =========================
    def get_permissions(self):

        # seul patient peut créer
        if self.action == "create":
            return [IsPatient()]

        # seul pharmacien peut modifier statut
        if self.action in ("update", "partial_update"):
            return [IsPharmacien()]

        # lecture pour utilisateur connecté
        return [IsAuthenticated()]

    # =========================
    # FILTRAGE DONNÉES
    # =========================
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # admin voit tout
        if _is_admin(user):
            return qs

        # pharmacien voit réservations de sa pharmacie
        if _is_pharmacien(user):
            return qs.filter(pharmacie__responsable=user)

        # patient voit uniquement ses réservations
        return qs.filter(user=user)

    # =========================
    # CREATE RESERVATION
    # =========================
    def perform_create(self, serializer):
        # on force l'utilisateur connecté comme propriétaire
        serializer.save(user=self.request.user)
