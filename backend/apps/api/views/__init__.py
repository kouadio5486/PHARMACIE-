"""
Package views — un fichier par ressource API.
"""
from .ai_views import AIInteractionViewSet
from .auth_views import EmailTokenObtainPairView
from .chats_views import ChatViewSet
from .deliveries_views import DeliveryViewSet
from .medicaments_views import MedicamentViewSet
from .notifications_views import NotificationViewSet
from .ordonnances_views import OrdonnanceViewSet
from .payments_views import PaymentViewSet
from .pharmacies_views import PharmacieViewSet
from .reservations_views import ReservationViewSet
from .stocks_views import StockViewSet
from .users_views import UserViewSet
from .villes_views import VilleViewSet

__all__ = [
    "AIInteractionViewSet",
    "ChatViewSet",
    "DeliveryViewSet",
    "EmailTokenObtainPairView",
    "MedicamentViewSet",
    "NotificationViewSet",
    "OrdonnanceViewSet",
    "PaymentViewSet",
    "PharmacieViewSet",
    "ReservationViewSet",
    "StockViewSet",
    "UserViewSet",
    "VilleViewSet",
]
