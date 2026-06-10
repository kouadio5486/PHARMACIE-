"""
Package serializers — un fichier par domaine métier.
"""
from .ai_serializers import AIInteractionCreateSerializer, AIInteractionSerializer
from .auth_serializers import ChangePasswordSerializer, EmailTokenObtainPairSerializer
from .chats_serializers import ChatCreateSerializer, ChatSerializer
from .deliveries_serializers import (
    DeliveryCreateSerializer,
    DeliveryGpsUpdateSerializer,
    DeliverySerializer,
)
from .medicaments_serializers import (
    MedicamentAuthenticiteSerializer,
    MedicamentComparaisonPrixSerializer,
    MedicamentDetailSerializer,
    MedicamentDisponibiliteSerializer,
    MedicamentListSerializer,
    MedicamentSerializer,
    MedicamentVerifyQrSerializer,
    StockDisponibiliteSerializer,
)
from .notifications_serializers import (
    NotificationMarkReadSerializer,
    NotificationSerializer,
)
from .ordonnances_serializers import (
    OrdonnanceSerializer,
    OrdonnanceUploadSerializer,
    OrdonnanceValidationSerializer,
)
from .payments_serializers import PaymentCreateSerializer, PaymentSerializer
from .pharmacies_serializers import (
    PharmacieListSerializer,
    PharmacieProcheQuerySerializer,
    PharmacieProcheSerializer,
    PharmacieSerializer,
)
from .reservations_serializers import (
    ReservationCreateSerializer,
    ReservationSerializer,
    ReservationStatutSerializer,
)
from .stocks_serializers import StockDetailSerializer, StockSerializer
from .users_serializers import (
    UserCreateSerializer,
    UserPublicSerializer,
    UserSerializer,
)
from .villes_serializers import VilleSerializer

__all__ = [
    "AIInteractionCreateSerializer",
    "AIInteractionSerializer",
    "ChangePasswordSerializer",
    "ChatCreateSerializer",
    "ChatSerializer",
    "DeliveryCreateSerializer",
    "DeliveryGpsUpdateSerializer",
    "DeliverySerializer",
    "EmailTokenObtainPairSerializer",
    "MedicamentAuthenticiteSerializer",
    "MedicamentComparaisonPrixSerializer",
    "MedicamentDetailSerializer",
    "MedicamentDisponibiliteSerializer",
    "MedicamentListSerializer",
    "MedicamentSerializer",
    "MedicamentVerifyQrSerializer",
    "NotificationMarkReadSerializer",
    "NotificationSerializer",
    "OrdonnanceSerializer",
    "OrdonnanceUploadSerializer",
    "OrdonnanceValidationSerializer",
    "PaymentCreateSerializer",
    "PaymentSerializer",
    "PharmacieListSerializer",
    "PharmacieProcheQuerySerializer",
    "PharmacieProcheSerializer",
    "PharmacieSerializer",
    "ReservationCreateSerializer",
    "ReservationSerializer",
    "ReservationStatutSerializer",
    "StockDetailSerializer",
    "StockDisponibiliteSerializer",
    "StockSerializer",
    "UserCreateSerializer",
    "UserPublicSerializer",
    "UserSerializer",
    "VilleSerializer",
]
