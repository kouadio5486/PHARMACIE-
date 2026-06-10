from rest_framework import serializers

from apps.pharmacies.models import Ville


class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = (
            "id",
            "nom",
            "code",
            "slug",
            "district",
            "region",
            "latitude",
            "longitude",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")
