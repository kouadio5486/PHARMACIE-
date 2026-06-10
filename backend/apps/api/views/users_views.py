"""API utilisateurs — rôles : patient, pharmacien, livreur, admin."""
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..permissions import IsAdmin, _is_admin
from ..serializers.users_serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Permissions (admin.py / spec) :
    - patient → recherche, réservation, ordonnance
    - pharmacien → stock, validation, gestion pharmacie
    - livreur → livraison, GPS
    - admin → tout
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    search_fields = ("nom", "prenom", "email", "telephone")
    filterset_fields = ("role", "is_active", "is_verified")

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        if self.action in ("list", "destroy"):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if _is_admin(self.request.user):
            return qs
        return qs.filter(pk=self.request.user.pk)

    def perform_create(self, serializer):
        role = serializer.validated_data.get("role", User.ROLE_PATIENT)
        if role == User.ROLE_ADMIN and not _is_admin(self.request.user):
            role = User.ROLE_PATIENT
        serializer.save(role=role)
