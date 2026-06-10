from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Profil minimal (listes imbriquées, chat)."""

    class Meta:
        model = User
        fields = ("id", "nom", "prenom", "role", "photo")
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nom",
            "prenom",
            "email",
            "telephone",
            "role",
            "photo",
            "adresse",
            "is_active",
            "is_verified",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_verified", "created_at", "updated_at")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "nom",
            "prenom",
            "email",
            "telephone",
            "password",
            "role",
            "adresse",
        )

    def validate_role(self, value):
        request = self.context.get("request")
        if value == User.ROLE_ADMIN and request and not request.user.is_superuser:
            if getattr(request.user, "role", None) != User.ROLE_ADMIN:
                raise serializers.ValidationError(
                    "Seul un administrateur peut créer un compte admin."
                )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
