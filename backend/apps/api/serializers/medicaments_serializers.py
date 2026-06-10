from rest_framework import serializers
# Import du modèle Medicament (table des médicaments)
from apps.medicaments.models import Medicament
# Import du modèle Ville (pour filtrer par localisation)
from apps.pharmacies.models import Ville
# Import du modèle Stock (relation médicament - pharmacie)
from apps.stocks.models import Stock
# Serializer pour afficher les infos d’une pharmacie
from .pharmacies_serializers import PharmacieListSerializer
from .villes_serializers import VilleSerializer


class VilleMedicamentQuerySerializer(serializers.Serializer):
    """Filtre optionnel par ville (ex. Yamoussoukro)."""

    ville = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.filter(is_active=True),
        required=False,
    )
     # Nom de la ville envoyé en texte (ex: "Abidjan")
    ville_nom = serializers.CharField(
        required=False,
        help_text="Ex. Yamoussoukro, Bouaké, M'batto",
    )

    def validate(self, attrs):
        # Récupère la ville si elle est envoyée
        ville = attrs.get("ville")
         # Récupère le nom de la ville si envoyé en texte
        ville_nom = attrs.get("ville_nom")
         # Si on a un nom mais pas d'objet ville
        if ville_nom and not ville:
            # Nettoie du texte le nom de la ville
            nom = ville_nom.strip()
            # Recherche la ville dans la base de données
            ville = Ville.objects.filter(
                nom__icontains=nom, is_active=True
            ).first()
            # Si aucune ville trouvée → erreur
            if not ville:
                raise serializers.ValidationError(
                    {"ville_nom": f"Aucune ville trouvée pour « {nom} »."}
                )
                # On remplace par l'objet ville trouvé
            attrs["ville"] = ville
        return attrs


class MedicamentListSerializer(serializers.ModelSerializer):
    """Résultat de recherche médicament."""
 # Nombre de pharmacies qui ont ce médicament
    nb_pharmacies = serializers.SerializerMethodField()
    # Prix minimum du médicament dans une pharmacie
    prix_min = serializers.SerializerMethodField()

    class Meta:
        model = Medicament
        fields = (
            "id",
            "nom",
            "dosage",
            "categorie",
            "laboratoire",
            "image",
            "ordonnance_requise",
            "nb_pharmacies",
            "prix_min",
        )
         # Tous ces champs sont en lecture seule
        # c'est-à-dire qu'ils ne peuvent pas être modifiés depuis l'API
        read_only_fields = fields

    # Récupère les stocks disponibles pour le médicament
    def _stocks_qs(self, obj):
        qs = obj.stocks.filter(quantite__gt=0, pharmacie__is_active=True)
        ville = self.context.get("ville")
        if ville:
            qs = qs.filter(pharmacie__ville=ville)
        return qs

    def get_nb_pharmacies(self, obj):
        
        return self._stocks_qs(obj).count()

    def get_prix_min(self, obj):
        # On trie par prix croissant
        stock = self._stocks_qs(obj).order_by("prix").first()
         # Si stock existe → retourne prix sinon None
        return stock.prix if stock else None


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = (
            "id",
            "nom",
            "description",
            "dosage",
            "categorie",
            "laboratoire",
            "image",
            "qr_code",
            "ordonnance_requise",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class MedicamentDetailSerializer(MedicamentSerializer):
    """Fiche médicament avec résumé disponibilité."""

    nb_pharmacies_disponibles = serializers.SerializerMethodField()
    prix_min = serializers.SerializerMethodField()
    prix_max = serializers.SerializerMethodField()

    class Meta(MedicamentSerializer.Meta):
        fields = MedicamentSerializer.Meta.fields + (
            "nb_pharmacies_disponibles",
            "prix_min",
            "prix_max",
        )

    def _stocks_disponibles(self, obj):
        qs = obj.stocks.filter(quantite__gt=0, pharmacie__is_active=True)
        ville = self.context.get("ville")
        if ville:
            qs = qs.filter(pharmacie__ville=ville)
        return qs

    def get_nb_pharmacies_disponibles(self, obj):
         # Nombre de pharmacies disponibles
        return self._stocks_disponibles(obj).count()

    def get_prix_min(self, obj):
        stock = self._stocks_disponibles(obj).order_by("prix").first()
        return stock.prix if stock else None

    def get_prix_max(self, obj):
        stock = self._stocks_disponibles(obj).order_by("-prix").first()
        return stock.prix if stock else None


class StockDisponibiliteSerializer(serializers.ModelSerializer):
    """Où le médicament est disponible + prix (comparaison)."""

    pharmacie = PharmacieListSerializer(read_only=True)
    # Champ calculé
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = (
            "id",
            "pharmacie",
            "quantite",
            "prix",
            "disponible",
            "stock_faible",
            "date_mise_a_jour",
        )
        read_only_fields = fields

    def get_disponible(self, obj):
        return obj.quantite > 0 and obj.pharmacie.is_active


class MedicamentDisponibiliteSerializer(serializers.Serializer):
    medicament = MedicamentDetailSerializer(read_only=True)
    disponibilites = StockDisponibiliteSerializer(many=True, read_only=True)
    total_pharmacies = serializers.IntegerField(read_only=True)

# COMPARAISON DES PRIX DES MÉDICAMENTS
class MedicamentComparaisonPrixSerializer(serializers.Serializer):
    medicament = MedicamentListSerializer(read_only=True)
    comparaison = StockDisponibiliteSerializer(many=True, read_only=True)
    prix_le_moins_cher = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, allow_null=True
    )
    prix_le_plus_cher = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, allow_null=True
    )


class MedicamentVerifyQrSerializer(serializers.Serializer):
    qr_code = serializers.CharField(max_length=255)

    def validate_qr_code(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Le code QR est obligatoire.")
        return value


class MedicamentAuthenticiteSerializer(serializers.Serializer):
    authentique = serializers.BooleanField()
    medicament = MedicamentSerializer(allow_null=True)
    message = serializers.CharField()
