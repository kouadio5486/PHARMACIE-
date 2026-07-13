from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("montant", models.DecimalField(max_digits=12, decimal_places=2, help_text="Montant payé en FCFA", verbose_name="Montant")),
                ("methode", models.CharField(choices=[("orange_money", "Orange Money"), ("mtn", "MTN Mobile Money"), ("wave", "Wave"), ("carte", "Carte Bancaire")], max_length=20, verbose_name="Méthode de paiement")),
                ("statut", models.CharField(choices=[("pending", "En attente"), ("success", "Succès"), ("failed", "Échec")], default="pending", max_length=20, verbose_name="Statut")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("reservation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="reservations.reservation", verbose_name="Réservation")),
            ],
            options={
                "db_table": "payments",
                "verbose_name": "Paiement",
                "verbose_name_plural": "Paiements",
                "ordering": ["-created_at"],
            },
        ),
    ]
