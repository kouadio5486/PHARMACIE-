"""API villes — liste des villes de Côte d'Ivoire."""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.pharmacies.models import Ville

from ..permissions import IsAdmin
from ..serializers.villes_serializers import VilleSerializer


class VilleViewSet(viewsets.ModelViewSet):
    """
    Référentiel des villes de Côte d'Ivoire.
    - lecture : tous
    - écriture : admin uniquement
    """

    queryset = Ville.objects.filter(is_active=True).order_by("nom")
    serializer_class = VilleSerializer
    search_fields = ("nom", "code", "district", "region", "slug")
    filterset_fields = ("is_active", "district", "region")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        if self.action in ("list", "retrieve") and not self.request.user.is_authenticated:
            return Ville.objects.filter(is_active=True).order_by("nom")
        if getattr(self.request.user, "role", None) == "admin" or self.request.user.is_superuser:
            return Ville.objects.all().order_by("nom")
        return Ville.objects.filter(is_active=True).order_by("nom")
