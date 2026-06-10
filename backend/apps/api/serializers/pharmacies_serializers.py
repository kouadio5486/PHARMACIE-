from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.pharmacies.models import Pharmacie, Ville

from .users_serializers import UserPublicSerializer
from .villes_serializers import VilleSerializer
# Récupère le modèle User personnalisé du projet
User = get_user_model()


class PharmacieListSerializer(serializers.ModelSerializer):
    """Liste / carte — localisation des pharmacies proches."""
# Affiche les infos de la ville (nom, etc.)
    ville = VilleSerializer(read_only=True)

    class Meta:
        model = Pharmacie
        fields = (
            "id",
            "nom",
            "ville",
            "adresse",
            "commune",
            "telephone",
            "latitude",
            "longitude",
            "horaire_ouverture",
            "horaire_fermeture",
            "is_active",
            "is_pharmacie_de_garde",
            "note_moyenne",
            "image",
        )
        read_only_fields = fields


class PharmacieProcheSerializer(PharmacieListSerializer):
    # Distance calculée côté backend (ex: 2.5 km)
    distance_km = serializers.FloatField(read_only=True)
 # On ajoute la distance à la liste normale
    class Meta(PharmacieListSerializer.Meta):
        fields = PharmacieListSerializer.Meta.fields + ("distance_km",)
        read_only_fields = fields


class PharmacieProcheQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
     # Rayon de recherche (ex: 10 km)
    rayon_km = serializers.FloatField(
        required=False,
        default=10.0,
        min_value=0.5,
        max_value=100.0,
        help_text="Rayon de recherche en kilomètres (défaut : 10).",
    )
    # Filtre par ville (ex: Abidjan, Bouaké, Yamoussoukro)
    ville = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.filter(is_active=True),
        required=False,
        help_text="Filtrer par ville (ex. Abidjan, Bouaké, Yamoussoukro).",
    )


class PharmacieSerializer(serializers.ModelSerializer):
    responsable = UserPublicSerializer(read_only=True)
    ville = VilleSerializer(read_only=True)
    responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.ROLE_PHARMACIEN),
        source="responsable",
        write_only=True,
        required=False,
    )
     # ID de la ville (écriture uniquement)
    ville_id = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.filter(is_active=True),
        source="ville",
        write_only=True,
    )

    class Meta:
        model = Pharmacie
        fields = (
            "id",
            "responsable",
            "responsable_id",
            "nom",
            "ville",
            "ville_id",
            "adresse",
            "commune",
            "telephone",
            "email",
            "latitude",
            "longitude",
            "horaire_ouverture",
            "horaire_fermeture",
            "is_active",
            "is_pharmacie_de_garde",
            "note_moyenne",
            "image",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "note_moyenne", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         # Si on modifie une pharmacie existante
        if self.instance is not None:
             # On empêche la modification du responsable
            self.fields.pop("responsable_id", None)
             # On empêche la modification de la ville
            self.fields.pop("ville_id", None)
