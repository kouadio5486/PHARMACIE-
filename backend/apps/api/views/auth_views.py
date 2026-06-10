"""Authentification JWT (login, refresh)."""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# - connexion avec email
# - ajout des informations utilisateur dans le token
from ..serializers.auth_serializers import EmailTokenObtainPairSerializer

# Vue de connexion personnalisée
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# Rend ces vues disponibles lors des imports
__all__ = ["EmailTokenObtainPairView", "TokenRefreshView"]
