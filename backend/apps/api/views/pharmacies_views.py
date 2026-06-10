"""API pharmacies — GPS, pharmacies proches."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.pharmacies.models import Pharmacie

# Permissions (contrôle accès selon rôle)
from ..permissions import IsAdmin, IsPharmacien, _is_admin, _is_pharmacien

# Fonction utilitaire pour filtrer par ville (?ville= ou ?ville_nom=)
from .common import get_ville_from_request

# Serializers (formats JSON différents selon cas)
from ..serializers.pharmacies_serializers import (
    PharmacieListSerializer,
    PharmacieProcheQuerySerializer,
    PharmacieProcheSerializer,
    PharmacieSerializer,
)

# Fonction pour calcul distance GPS (km)
from ..serializers.utils import haversine_km


class PharmacieViewSet(viewsets.ModelViewSet):
    """
    API Pharmacie :

    ✔ Admin → toutes les pharmacies
    ✔ Pharmacien → gère sa pharmacie
    ✔ Patient → voit pharmacies actives + proches

    Fonctionnalités :
    - liste pharmacies
    - détails pharmacie
    - filtrage par ville
    - recherche GPS pharmacies proches
    """

    # Optimisation requête (évite requêtes multiples SQL)
    queryset = Pharmacie.objects.select_related("responsable", "ville").all()

    # filtres automatiques API
    filterset_fields = ("ville", "commune", "is_active", "is_pharmacie_de_garde")
    search_fields = ("nom", "commune", "adresse", "ville__nom")
    ordering_fields = ("nom", "note_moyenne", "created_at")

    # =========================
    # CHOIX DU SERIALIZER
    # =========================
    def get_serializer_class(self):
        # endpoint spécial GPS
        if self.action == "proches":
            return PharmacieProcheSerializer

        # liste simple
        if self.action == "list":
            return PharmacieListSerializer

        # détail / create / update
        return PharmacieSerializer

    # =========================
    # GESTION DES PERMISSIONS
    # =========================
    def get_permissions(self):
        # lecture autorisée à tous utilisateurs connectés
        if self.action in ("list", "retrieve", "proches"):
            return [IsAuthenticated()]

        # pharmacien peut gérer ses données
        if _is_pharmacien(self.request.user):
            return [IsPharmacien()]

        # sinon admin
        return [IsAdmin()]

    # =========================
    # FILTRAGE DES DONNÉES
    # =========================
    def get_queryset(self):
        base_queryset = super().get_queryset()
        user = self.request.user

        # récupération ville (?ville= ou ?ville_nom=)
        ville = get_ville_from_request(self.request)

        # admin voit tout
        if _is_admin(user):
            filtered_queryset = base_queryset

        # pharmacien voit seulement ses pharmacies
        elif _is_pharmacien(user):
            filtered_queryset = base_queryset.filter(responsable=user)

        # patient voit seulement pharmacies actives
        else:
            filtered_queryset = base_queryset.filter(is_active=True)

        # filtre supplémentaire par ville
        if ville is not None:
            filtered_queryset = filtered_queryset.filter(ville=ville)

        return filtered_queryset

    # =========================
    # CREATION PHARMACIE
    # =========================
    def perform_create(self, serializer):
        # si pharmacien → auto assigné comme responsable
        if _is_pharmacien(self.request.user) and not _is_admin(self.request.user):
            serializer.save(responsable=self.request.user)
        else:
            serializer.save()

    # =========================
    # ENDPOINT GPS : pharmacies proches
    # =========================
    @action(detail=False, methods=["get"], url_path="proches")
    def proches(self, request):
        """
        GET /api/pharmacies/proches/?latitude=...&longitude=...&rayon_km=10

        ➜ retourne les pharmacies proches du patient
        """

        # validation des paramètres GPS
        query = PharmacieProcheQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        lat = query.validated_data["latitude"]
        lon = query.validated_data["longitude"]
        rayon = query.validated_data["rayon_km"]
        ville = query.validated_data.get("ville")

        # base queryset filtré
        queryset = self.get_queryset().filter(is_active=True)

        # filtre par ville si fourni
        if ville is not None:
            queryset = queryset.filter(ville=ville)

        pharmacies_proches = []

        # calcul distance GPS pour chaque pharmacie
        for pharmacie in queryset:
            distance_km = haversine_km(
                lat,
                lon,
                pharmacie.latitude,
                pharmacie.longitude
            )

            # garder uniquement celles dans le rayon
            if distance_km <= rayon:
                pharmacie.distance_km = round(distance_km, 2)
                pharmacies_proches.append(pharmacie)

        # tri par distance (plus proche d'abord)
        pharmacies_proches.sort(key=lambda p: p.distance_km)

        # conversion en JSON
        serializer = PharmacieProcheSerializer(pharmacies_proches, many=True)

        return Response(serializer.data)