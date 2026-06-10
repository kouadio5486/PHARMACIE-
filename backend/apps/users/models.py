from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Manager personnalisé
class UserManager(BaseUserManager):

    def create_user(self, email, nom, prenom, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            **extra_fields
        )

        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, nom, prenom, password, **extra_fields)


#  MODELE USER
class User(AbstractBaseUser, PermissionsMixin):

    ROLE_PATIENT = "patient"
    ROLE_PHARMACIEN = "pharmacien"
    ROLE_LIVREUR = "livreur"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = (
        (ROLE_PATIENT, "Patient"),
        (ROLE_PHARMACIEN, "Pharmacien"),
        (ROLE_LIVREUR, "Livreur"),
        (ROLE_ADMIN, "Admin"),
    )

    id = models.AutoField(primary_key=True)

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # password géré automatiquement par AbstractBaseUser
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    photo = models.ImageField(upload_to="users/", blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    class Meta:
        db_table = "users_user"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"