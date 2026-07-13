from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pharmacies", "0002_add_ville_and_update_pharmacie"),
        ("medicaments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantite", models.PositiveIntegerField(default=0, verbose_name="Quantité disponible")),
                ("prix", models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix du médicament dans cette pharmacie", verbose_name="Prix (FCFA)")),
                ("seuil_alerte", models.PositiveIntegerField(default=5, help_text="Quantité minimale avant déclenchement d'une alerte", verbose_name="Seuil d'alerte")),
                ("date_mise_a_jour", models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("medicament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stocks", to="medicaments.medicament", verbose_name="Médicament")),
                ("pharmacie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stocks", to="pharmacies.pharmacie", verbose_name="Pharmacie")),
            ],
            options={
                "db_table": "stocks",
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
                "ordering": ["pharmacie", "medicament"],
                "constraints": [
                    models.UniqueConstraint(fields=["pharmacie", "medicament"], name="unique_stock_par_pharmacie_medicament")
                ],
            },
        ),
    ]
