# Comme tu as créé un User personnalisé avec AbstractBaseUser,
# cette fonction retournera TON modèle User et non celui par défaut de Django.
from django.contrib.auth import get_user_model
# - valider les données reçues du frontend
# - convertir des objets Python en JSON
# - convertir du JSON en objets Python
from rest_framework import serializers

# Importe le serializer JWT fourni par Simple JWT.
#
# Ce serializer gère automatiquement :
# - la vérification de l'utilisateur
# - la vérification du mot de passe
# - la génération des tokens JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# User contiendra donc ton modèle personnalisé.
User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Connexion JWT avec l'email (USERNAME_FIELD)."""

    @classmethod
    # Son rôle est d'ajouter des informations
    # personnalisées à l'intérieur du token.
    def get_token(cls, user):
        # On appelle le serializer parent pour générer le token.
        token = super().get_token(user)
        # On ajoute les informations personnalisées au token.
        token["role"] = user.role
        token["email"] = user.email
        token["nom"] = user.nom
        token["prenom"] = user.prenom
        # On retourne le token avec les informations personnalisées.
        return token

    # On redéfinit le __init__ pour utiliser l'email comme identifiant.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = self.fields.pop("username")

    # On redéfinit la méthode validate pour inclure les informations personnalisées.
    def validate(self, attrs):
        # On appelle la méthode validate du parent pour valider les données.
        data = super().validate(attrs)
        # On ajoute les informations personnalisées à la réponse.
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "nom": self.user.nom,
            "prenom": self.user.prenom,
            "role": self.user.role,
        }
        # On retourne la réponse avec les informations personnalisées.
        return data

    # On crée un serializer pour changer le mot de passe.
class ChangePasswordSerializer(serializers.Serializer):
    # On crée un champ pour le mot de passe actuel.
    ancien_mot_de_passe = serializers.CharField(write_only=True)
    # On crée un champ pour le nouveau mot de passe.
    nouveau_mot_de_passe = serializers.CharField(write_only=True, min_length=8)

    def validate_ancien_mot_de_passe(self, value):
        # On récupère l'utilisateur connecté.
        user = self.context["request"].user
        # On vérifie si le mot de passe actuel est correct.
        if not user.check_password(value):
            # On renvoie une erreur si le mot de passe actuel est incorrect.
            raise serializers.ValidationError("Mot de passe actuel incorrect.")
        return value
