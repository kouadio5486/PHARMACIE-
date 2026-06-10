from rest_framework import serializers
from apps.stocks.models import Stock

from .medicaments_serializers import MedicamentListSerializer
from .pharmacies_serializers import PharmacieListSerializer


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer principal des stocks.

    Permet :
    - création / modification stock (pharmacien)
    - affichage simple (liste API)
    """

    medicament_nom = serializers.CharField(source="medicament.nom", read_only=True)
    pharmacie_nom = serializers.CharField(source="pharmacie.nom", read_only=True)

    stock_faible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = (
            "id",
            "pharmacie",
            "medicament",
            "medicament_nom",
            "pharmacie_nom",
            "quantite",
            "prix",
            "seuil_alerte",
            "stock_faible",
            "date_mise_a_jour",
            "created_at",
        )
        read_only_fields = (
            "id",
            "date_mise_a_jour",
            "created_at",
            "stock_faible"
        )

    # ==================================================
    # 🔒 VALIDATION MÉTIER (ANTI-DOUBLON)
    # ==================================================
    def validate(self, attrs):
        pharmacie = attrs.get("pharmacie") or getattr(self.instance, "pharmacie", None)
        medicament = attrs.get("medicament") or getattr(self.instance, "medicament", None)

        if pharmacie and medicament:
            qs = Stock.objects.filter(
                pharmacie=pharmacie,
                medicament=medicament
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    "Ce médicament existe déjà dans cette pharmacie."
                )

        return attrs

    # ==================================================
    # ⚡ AMÉLIORATION PRO : sécurité quantité
    # ==================================================
    def validate_quantite(self, value):
        """
        Empêche des valeurs incohérentes (optionnel mais propre)
        """
        if value < 0:
            raise serializers.ValidationError("La quantité ne peut pas être négative.")
        return value

    # ==================================================
    # ⚡ AMÉLIORATION PRO : prix sécurité
    # ==================================================
    def validate_prix(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être supérieur à 0.")
        return value


class StockDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé (lecture uniquement)
    """

    medicament = MedicamentListSerializer(read_only=True)
    pharmacie = PharmacieListSerializer(read_only=True)
    stock_faible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = (
            "id",
            "pharmacie",
            "medicament",
            "quantite",
            "prix",
            "seuil_alerte",
            "stock_faible",
            "date_mise_a_jour",
            "created_at",
        )
        read_only_fields = fields