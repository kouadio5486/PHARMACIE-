from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.pharmacies.models import Pharmacie, Ville

from .users_serializers import UserPublicSerializer
from .villes_serializers import VilleSerializer
# Récupère le modèle User personnalisé du projet
User = get_user_model()


class PharmacieListSerializer(serializers.ModelSerializer):
    """Liste / carte — localisation des pharmacies proches."""

    ville = VilleSerializer(read_only=True)
    localite_affichage = serializers.SerializerMethodField(
        help_text="Localité finale affichée : Ville référencée OU localité libre (village)."
    )

    class Meta:
        model = Pharmacie
        fields = (
            "id",
            "nom",
            "ville",
            "localite_libre",
            "localite_affichage",
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

    def get_localite_affichage(self, obj):
        """
        Priorité d'affichage :
        1. Ville référencée dans la table (si présente)
        2. localite_libre (nom du village tapé à la main)
        """
        if obj.ville:
            return obj.ville.nom
        if obj.localite_libre:
            return obj.localite_libre
        return None


class PharmacieProcheSerializer(PharmacieListSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta(PharmacieListSerializer.Meta):
        fields = PharmacieListSerializer.Meta.fields + ("distance_km",)
        read_only_fields = fields


class PharmacieProcheQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    rayon_km = serializers.FloatField(
        required=False,
        default=10.0,
        min_value=0.5,
        max_value=100.0,
        help_text="Rayon de recherche en kilomètres (défaut : 10).",
    )
    ville = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.filter(is_active=True),
        required=False,
        help_text="Filtrer par localité référencée (ville/commune/village).",
    )
    localite = serializers.CharField(
        required=False,
        help_text="Recherche texte libre dans localite_libre, commune ou nom de la ville (ex: Tiébissou, Kouto, Cocody).",
    )


class PharmacieSerializer(serializers.ModelSerializer):
    responsable = UserPublicSerializer(read_only=True)
    ville = VilleSerializer(read_only=True)
    localite_affichage = serializers.SerializerMethodField()

    responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.ROLE_PHARMACIEN),
        source="responsable",
        write_only=True,
        required=False,
    )
    ville_id = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.filter(is_active=True),
        source="ville",
        write_only=True,
        required=False,
        allow_null=True,
        help_text="ID de la localité référencée. Peut être NULL si on utilise localite_libre (village non référencé).",
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
            "localite_libre",
            "localite_affichage",
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
        read_only_fields = ("id", "note_moyenne", "localite_affichage", "created_at", "updated_at")

    def get_localite_affichage(self, obj):
        if obj.ville:
            return obj.ville.nom
        if obj.localite_libre:
            return obj.localite_libre
        return None

    def validate(self, attrs):
        """
        Règle métier : soit ville_id est renseigné,
        soit localite_libre est renseigné. Les deux peuvent aussi être présents.
        Mais on refuse que les deux soient vides.
        """
        ville = attrs.get("ville") or (self.instance.ville if self.instance else None)
        localite_libre = attrs.get("localite_libre") or (self.instance.localite_libre if self.instance else None)
        if not ville and not localite_libre:
            raise serializers.ValidationError(
                "Vous devez renseigner soit une localité (ville/commune/village) dans la liste, "
                "soit le champ « localite_libre » pour un village non référencé."
            )
        return attrs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.pop("responsable_id", None)
            self.fields.pop("ville_id", None)
