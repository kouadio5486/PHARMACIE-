"""Charge les principales villes de Côte d'Ivoire (à lancer une fois après migrate)."""
from django.core.management.base import BaseCommand

from apps.pharmacies.models import Ville

VILLES_CI = [
    "Abidjan",
    "Bouaké",
    "Yamoussoukro",
    "San-Pédro",
    "Daloa",
    "Korhogo",
    "Man",
    "Gagnoa",
    "Divo",
    "M'batto",
    "Abengourou",
    "Agboville",
    "Bondoukou",
    "Odienné",
    "Séguéla",
    "Soubré",
    "Grand-Bassam",
    "Dabou",
    "Issia",
    "Bingerville",
]


class Command(BaseCommand):
    help = "Crée les villes de Côte d'Ivoire dans la table villes."

    def handle(self, *args, **options):
        created = 0
        for nom in VILLES_CI:
            _, was_created = Ville.objects.get_or_create(nom=nom)
            if was_created:
                created += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"{created} ville(s) créée(s). Total : {Ville.objects.count()}."
            )
        )
