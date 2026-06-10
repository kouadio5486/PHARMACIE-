"""
API stocks — gestion des quantités et prix par pharmacie.

Ce ViewSet permet de :
- consulter les stocks disponibles
- gérer les stocks (pharmacien)
- superviser les stocks (admin)
"""
#  AMÉLIORATION : sécurité des opérations critiques
from django.db import transaction  

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.stocks.models import Stock

from ..permissions import IsPharmacien, _is_admin, _is_pharmacien
from ..serializers.stocks_serializers import StockDetailSerializer, StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    ============================
    API STOCKS (pharmacie)
    ============================

    Rôle métier :
    - Pharmacien → gère son stock (CRUD)
    - Admin → supervision globale
    - Patient → consultation uniquement
    """

    queryset = Stock.objects.select_related("pharmacie", "medicament")

    filterset_fields = ("pharmacie", "medicament")
    search_fields = ("medicament__nom", "pharmacie__nom")
    ordering_fields = ("prix", "quantite", "date_mise_a_jour")

    # ==================================================
    # SERIALIZER
    # ==================================================
    def get_serializer_class(self):
        if self.action == "retrieve":
            return StockDetailSerializer
        return StockSerializer

    # ==================================================
    # PERMISSIONS
    # ==================================================
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsPharmacien()]

    # ==================================================
    # FILTRAGE PAR RÔLE
    # ==================================================
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if _is_admin(user):
            return qs

        if _is_pharmacien(user):
            return qs.filter(pharmacie__responsable=user)

        return qs.filter(
            pharmacie__is_active=True,
            quantite__gt=0
        )

    # ==================================================
    # AMÉLIORATION 1 : TRANSACTIONS (sécurité stock)
    # ==================================================
    @transaction.atomic
    def perform_update(self, serializer):
        """
        Garantit qu'une modification de stock est atomique.
        → évite incohérences si plusieurs requêtes simultanées
        """
        serializer.save()

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    # ==================================================
    #  AMÉLIORATION 2 : VERROUILLAGE CONCURRENCE
    # ==================================================
    def get_queryset(self):
        qs = super().get_queryset()

        # verrouillage léger pour éviter double écriture concurrente
        # (utile surtout lors des réservations)
        return qs.select_for_update(of=("self",))

    # ==================================================
    #  AMÉLIORATION 3 : LOGS (AUDIT SIMPLE)
    # ==================================================
    def perform_update(self, serializer):
        instance = serializer.save()

        # log simple (tu peux remplacer par modèle AuditLog)
        print(
            f"[AUDIT STOCK] user={self.request.user.id} "
            f"stock_id={instance.id} "
            f"quantite={instance.quantite} "
            f"prix={instance.prix}"
        )