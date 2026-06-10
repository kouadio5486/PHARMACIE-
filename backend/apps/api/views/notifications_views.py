"""API notifications — lecture par l'utilisateur."""
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notifications.models import Notification

from ..serializers.notifications_serializers import NotificationSerializer


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Permissions :
    - système → envoi (hors API publique / signaux admin)
    - user → lecture et marquer comme lu
    Types : info, alert, success
    """

    serializer_class = NotificationSerializer
    filterset_fields = ("type", "is_read")
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def get_permissions(self):
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="marquer-lu")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(NotificationSerializer(notification).data)
