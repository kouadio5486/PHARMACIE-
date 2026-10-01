from rest_framework import serializers

from apps.pharmacies.models import Ville


class VilleSerializer(serializers.ModelSerializer):
    """
    Sérialize une localité : Ville / Commune / Village.
    Le champ `type` permet de filtrer par catégorie dans le frontend.
    """

    type_display = serializers.CharField(
        source="get_type_display",
        read_only=True,
        help_text="Libellé du type : Ville, Commune ou Village.",
    )

    class Meta:
        model = Ville
        fields = (
            "id",
            "type",
            "type_display",
            "nom",
            "code",
            "slug",
            "district",
            "region",
            "population",
            "latitude",
            "longitude",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "type_display", "created_at", "updated_at")
