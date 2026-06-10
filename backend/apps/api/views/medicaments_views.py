"""API médicaments — recherche, disponibilité, prix, authenticité QR."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.medicaments.models import Medicament

from ..permissions import IsAdmin
from ..serializers.medicaments_serializers import (
    MedicamentAuthenticiteSerializer,
    MedicamentDetailSerializer,
    MedicamentListSerializer,
    MedicamentSerializer,
    MedicamentVerifyQrSerializer,
    StockDisponibiliteSerializer,
    VilleMedicamentQuerySerializer,
)
from ..serializers.villes_serializers import VilleSerializer
from .common import get_ville_from_request, prefetch_stocks_disponibles


class MedicamentViewSet(viewsets.ModelViewSet):
    """
    Recherche médicament + prix/disponibilité par ville (?ville= ou ?ville_nom=).

    Ex. à Yamoussoukro :
    - GET /api/medicaments/?ville_nom=Yamoussoukro&search=doliprane
    - GET /api/medicaments/1/disponibilite/?ville_nom=Yamoussoukro
    - GET /api/medicaments/1/comparer-prix/?ville_nom=Yamoussoukro
    """

    queryset = Medicament.objects.all().order_by("nom")
    filterset_fields = ("categorie", "ordonnance_requise", "laboratoire")
    search_fields = ("nom", "laboratoire", "categorie", "dosage")
    ordering_fields = ("nom", "created_at")

    def _ville_context(self):
        ville = get_ville_from_request(self.request)
        return {"ville": ville, "request": self.request}

    def get_serializer_context(self):
        return {**super().get_serializer_context(), **self._ville_context()}

    def get_serializer_class(self):
        if self.action == "list":
            return MedicamentListSerializer
        if self.action == "retrieve":
            return MedicamentDetailSerializer
        if self.action == "verifier_qr":
            return MedicamentVerifyQrSerializer
        return MedicamentSerializer

    def get_permissions(self):
        if self.action in (
            "list",
            "retrieve",
            "disponibilite",
            "comparer_prix",
            "verifier_qr",
        ):
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        ville = get_ville_from_request(self.request)
        if self.action in ("retrieve", "disponibilite", "comparer_prix"):
            return qs.prefetch_related(prefetch_stocks_disponibles(ville))
        return qs

    def _parse_ville_query(self):
        ser = VilleMedicamentQuerySerializer(data=self.request.query_params)
        ser.is_valid(raise_exception=True)
        return ser.validated_data.get("ville")

    def _stocks_disponibles(self, medicament, ville=None):
        if ville is None:
            ville = get_ville_from_request(self.request)
        qs = medicament.stocks.filter(quantite__gt=0, pharmacie__is_active=True)
        if ville:
            qs = qs.filter(pharmacie__ville=ville).select_related(
                "pharmacie", "pharmacie__ville"
            )
        return qs.order_by("prix")

    def _ville_payload(self, ville):
        if ville:
            return VilleSerializer(ville).data
        return None

    @action(detail=True, methods=["get"], url_path="disponibilite")
    def disponibilite(self, request, pk=None):
        """Pharmacies où le médicament est disponible (filtrable par ville)."""
        ville = self._parse_ville_query() or get_ville_from_request(request)
        medicament = self.get_object()
        stocks = self._stocks_disponibles(medicament, ville=ville)
        ctx = {"ville": ville}
        return Response(
            {
                "ville": self._ville_payload(ville),
                "medicament": MedicamentDetailSerializer(
                    medicament, context=ctx
                ).data,
                "disponibilites": StockDisponibiliteSerializer(
                    stocks, many=True
                ).data,
                "total_pharmacies": stocks.count(),
            }
        )

    @action(detail=True, methods=["get"], url_path="comparer-prix")
    def comparer_prix(self, request, pk=None):
        """Comparer les prix entre pharmacies d'une même ville."""
        ville = self._parse_ville_query() or get_ville_from_request(request)
        medicament = self.get_object()
        stocks = list(self._stocks_disponibles(medicament, ville=ville))
        prix_list = [s.prix for s in stocks]
        ctx = {"ville": ville}
        return Response(
            {
                "ville": self._ville_payload(ville),
                "medicament": MedicamentListSerializer(
                    medicament, context=ctx
                ).data,
                "comparaison": StockDisponibiliteSerializer(
                    stocks, many=True
                ).data,
                "prix_le_moins_cher": min(prix_list) if prix_list else None,
                "prix_le_plus_cher": max(prix_list) if prix_list else None,
            }
        )

    @action(detail=False, methods=["post"], url_path="verifier-qr")
    def verifier_qr(self, request):
        """Vérifier l'authenticité via le QR code unique du médicament."""
        ser = MedicamentVerifyQrSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        qr = ser.validated_data["qr_code"]

        try:
            medicament = Medicament.objects.get(qr_code=qr)
            payload = {
                "authentique": True,
                "medicament": MedicamentSerializer(medicament).data,
                "message": "Médicament authentique enregistré sur PharmaCI.",
            }
        except Medicament.DoesNotExist:
            payload = {
                "authentique": False,
                "medicament": None,
                "message": "Code QR inconnu — médicament non reconnu.",
            }

        return Response(MedicamentAuthenticiteSerializer(payload).data)
