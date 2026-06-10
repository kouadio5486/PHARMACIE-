from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AIInteractionViewSet,
    ChatViewSet,
    DeliveryViewSet,
    EmailTokenObtainPairView,
    MedicamentViewSet,
    NotificationViewSet,
    OrdonnanceViewSet,
    PaymentViewSet,
    PharmacieViewSet,
    ReservationViewSet,
    StockViewSet,
    UserViewSet,
    VilleViewSet,
)

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"villes", VilleViewSet, basename="ville")
router.register(r"pharmacies", PharmacieViewSet, basename="pharmacie")
router.register(r"medicaments", MedicamentViewSet, basename="medicament")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"deliveries", DeliveryViewSet, basename="delivery")
router.register(r"ordonnances", OrdonnanceViewSet, basename="ordonnance")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"chats", ChatViewSet, basename="chat")
router.register(r"ai", AIInteractionViewSet, basename="ai")

urlpatterns = [
    path("auth/login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
