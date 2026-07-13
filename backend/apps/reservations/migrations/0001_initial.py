from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("pharmacies", "0002_add_ville_and_update_pharmacie"),
        ("medicaments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantite", models.PositiveIntegerField(verbose_name="Quantité")),
                ("statut", models.CharField(choices=[("pending", "En attente"), ("confirmed", "Confirmée"), ("cancelled", "Annulée"), ("done", "Terminée")], default="pending", max_length=20, verbose_name="Statut")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("medicament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to="medicaments.medicament", verbose_name="Médicament")),
                ("pharmacie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to="pharmacies.pharmacie", verbose_name="Pharmacie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to="users.user", verbose_name="Utilisateur")),
            ],
            options={
                "db_table": "reservations",
                "verbose_name": "Réservation",
                "verbose_name_plural": "Réservations",
                "ordering": ["-created_at"],
            },
        ),
    ]
