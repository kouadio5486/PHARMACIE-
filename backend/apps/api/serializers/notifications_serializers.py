# Il permet de transformer les modèles Django en JSON pour l’API
from rest_framework import serializers
# Import du modèle Notification (table des notifications)
from apps.notifications.models import Notification

 # Champ calculé : transforme le "type" (code) en texte lisible
    # Exemple : "info" → "Information"
class NotificationSerializer(serializers.ModelSerializer):
     # méthode Django automatique (choices)
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
         # Champs envoyés au frontend (API)
        model = Notification
        fields = (
            "id",
            "user",
            "message",
            "type",
            "type_display",
            "is_read",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at", "type_display")


class NotificationMarkReadSerializer(serializers.ModelSerializer):
    class Meta:
        # On ne permet que la modification de "is_read"
        model = Notification
        fields = ("is_read",)
 # Validation du champ is_read
    def validate_is_read(self, value):
         # On force uniquement la valeur True
        # (pour éviter qu’un utilisateur remette False)
        if not value:
            raise serializers.ValidationError("Utilisez is_read=true pour marquer comme lu.")
        return value
