"""API paiements :
- Paiement médicaments → patient paie → l'argent va à la pharmacie.
- Paiement livraison → client paie → l'argent va au livreur (cash ou mobile money).
"""
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.payments.models import Payment
from apps.deliveries.models import Delivery
from apps.api.permissions import (
    IsAdmin,
    IsPatient,
    IsLivreur,
    IsPharmacien,
    _is_admin,
    _is_livreur,
    _is_pharmacien,
)
from apps.api.serializers.payments_serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Permissions :
    - patient   → créer un paiement de médicaments OU de livraison
    - livreur → créer un paiement de livraison (pour sa livraison)
    - pharmacien → voir paiements des médicaments de sa pharmacie
    - admin → tout voir + modifier statut
    """

    queryset = Payment.objects.select_related(
        "reservation", "reservation__user", "reservation__pharmacie",
        "delivery", "delivery__livreur",
    )
    filterset_fields = ("statut", "methode", "type_paiement", "reservation", "delivery")
    ordering_fields = ("created_at", "montant")
    http_method_names = ["get", "post", "head", "options", "patch", "put"]

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_permissions(self):
        if self.action == "create":
            # Patient, Livreur, Pharmacien (si livraison) peuvent créer.
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if _is_admin(user):
            return qs

        from django.db.models import Q
        # Visibilité suivant le rôle :
        q_patient = Q(reservation__user=user)
        q_livreur = Q(type_paiement=Payment.TYPE_LIVRAISON, delivery__livreur=user)
        q_pharmacien = Q(
            type_paiement=Payment.TYPE_MEDICAMENTS,
            reservation__pharmacie__responsable=user,
        )
        return qs.filter(q_patient | q_livreur | q_pharmacien)

    def perform_create(self, serializer):
        """
        Quand le paiement est créé en statut "success",
        on met aussi à jour la livraison (paiement livraison confirmé)
        et on renseigne paid_at.
        """
        from django.utils import timezone
        from apps.deliveries.models import Delivery

        instance = serializer.save()
        if instance.statut == Payment.STATUS_SUCCESS and not instance.paid_at:
            instance.paid_at = timezone.now()
            instance.save(update_fields=["paid_at"])

        if (
            instance.type_paiement == Payment.TYPE_LIVRAISON
            and instance.delivery_id
            and instance.statut == Payment.STATUS_SUCCESS
        ):
            Delivery.objects.filter(id=instance.delivery_id).update(
                statut_paiement_livraison=Delivery.PAIEMENT_PAYE,
            )
