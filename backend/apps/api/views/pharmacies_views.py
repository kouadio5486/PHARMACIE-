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
    - filtrage par localité référencée OU texte libre (village)
    - recherche GPS pharmacies proches
    """

    queryset = Pharmacie.objects.select_related("responsable", "ville").all()

    filterset_fields = ("ville", "commune", "is_active", "is_pharmacie_de_garde")
    search_fields = (
        "nom",
        "commune",
        "adresse",
        "ville__nom",
        "localite_libre",
    )
    ordering_fields = ("nom", "note_moyenne", "created_at")

    def get_serializer_class(self):
        if self.action == "proches":
            return PharmacieProcheSerializer
        if self.action == "list":
            return PharmacieListSerializer
        return PharmacieSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve", "proches"):
            return [IsAuthenticated()]
        if _is_pharmacien(self.request.user):
            return [IsPharmacien()]
        return [IsAdmin()]

    def get_queryset(self):
        from django.db.models import Q

        base_queryset = super().get_queryset()
        user = self.request.user

        ville = get_ville_from_request(self.request)
        localite_texte = self.request.query_params.get("localite")

        if _is_admin(user):
            qs = base_queryset
        elif _is_pharmacien(user):
            qs = base_queryset.filter(responsable=user)
        else:
            qs = base_queryset.filter(is_active=True)

        if ville is not None:
            qs = qs.filter(ville=ville)

        if localite_texte:
            terme = localite_texte.strip()
            """
            Recherche multi-niveaux (villes ET villages) :
            - Dans le nom de la localité référencée
            - Dans localite_libre (village non référencé)
            - Dans commune / quartier
            - Dans adresse
            """
            qs = qs.filter(
                Q(ville__nom__icontains=terme)
                | Q(localite_libre__icontains=terme)
                | Q(commune__icontains=terme)
                | Q(adresse__icontains=terme)
            )

        return qs

    def perform_create(self, serializer):
        if _is_pharmacien(self.request.user) and not _is_admin(self.request.user):
            serializer.save(responsable=self.request.user)
        else:
            serializer.save()

    @action(detail=False, methods=["get"], url_path="proches")
    def proches(self, request):
        """
        GET /api/pharmacies/proches/?latitude=...&longitude=...&rayon_km=10

        Paramètres supplémentaires :
        - ville : filtrer par localité référencée (ID)
        - localite : recherche texte dans localite_libre, commune, ville_nom
                     (ex: Tiébissou, Kouto, Cocody)

        ➜ retourne les pharmacies proches du patient, triées par distance.
        """
        from django.db.models import Q

        query = PharmacieProcheQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        lat = query.validated_data["latitude"]
        lon = query.validated_data["longitude"]
        rayon = query.validated_data["rayon_km"]
        ville = query.validated_data.get("ville")
        localite_texte = query.validated_data.get("localite")

        qs = self.get_queryset().filter(is_active=True)

        if ville is not None:
            qs = qs.filter(ville=ville)

        if localite_texte:
            terme = localite_texte.strip()
            qs = qs.filter(
                Q(ville__nom__icontains=terme)
                | Q(localite_libre__icontains=terme)
                | Q(commune__icontains=terme)
            )

        pharmacies_proches = []

        for pharmacie in qs:
            distance_km = haversine_km(
                lat,
                lon,
                pharmacie.latitude,
                pharmacie.longitude
            )
            if distance_km <= rayon:
                pharmacie.distance_km = round(distance_km, 2)
                pharmacies_proches.append(pharmacie)

        pharmacies_proches.sort(key=lambda p: p.distance_km)

        serializer = PharmacieProcheSerializer(pharmacies_proches, many=True)
        return Response(serializer.data)