"""API paiements — patient paie, admin vérifie."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.payments.models import Payment

from ..permissions import IsAdmin, IsPatient, _is_admin
from ..serializers.payments_serializers import PaymentCreateSerializer, PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Permissions :
    - patient → payer sa réservation
    - admin → vérification / modification statut
    Méthodes : orange_money, mtn, wave, carte
    Statuts : pending, success, failed
    """

    queryset = Payment.objects.select_related(
        "reservation", "reservation__user"
    )
    filterset_fields = ("statut", "methode")
    ordering_fields = ("created_at", "montant")
    http_method_names = ["get", "post", "head", "options", "patch", "put"]

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if _is_admin(user):
            return qs
        return qs.filter(reservation__user=user)
