from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("reservations", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Delivery",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("latitude", models.FloatField(blank=True, null=True, verbose_name="Latitude")),
                ("longitude", models.FloatField(blank=True, null=True, verbose_name="Longitude")),
                ("statut", models.CharField(choices=[("en_cours", "En cours"), ("livre", "Livré"), ("annule", "Annulé")], default="en_cours", max_length=20, verbose_name="Statut")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("livreur", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="deliveries", to="users.user", verbose_name="Livreur", limit_choices_to={"role": "livreur"})),
                ("reservation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="deliveries", to="reservations.reservation", verbose_name="Réservation")),
            ],
            options={
                "db_table": "deliveries",
                "verbose_name": "Livraison",
                "verbose_name_plural": "Livraisons",
                "ordering": ["-created_at"],
            },
        ),
    ]
