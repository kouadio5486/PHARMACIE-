from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Medicament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=255, verbose_name="Nom du médicament")),
                ("description", models.TextField(blank=True, null=True, verbose_name="Description")),
                ("dosage", models.CharField(max_length=100, help_text="Ex : 500mg, 1g, etc.", verbose_name="Dosage")),
                ("image", models.ImageField(blank=True, null=True, upload_to="medicaments/", verbose_name="Image")),
                ("laboratoire", models.CharField(max_length=255, verbose_name="Laboratoire")),
                ("qr_code", models.CharField(max_length=255, unique=True, help_text="Code unique permettant de vérifier l'authenticité du médicament.", verbose_name="QR Code")),
                ("categorie", models.CharField(blank=True, max_length=150, verbose_name="Catégorie")),
                ("ordonnance_requise", models.BooleanField(default=False, verbose_name="Ordonnance requise")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Date de modification")),
            ],
            options={
                "db_table": "medicaments",
                "verbose_name": "Médicament",
                "verbose_name_plural": "Médicaments",
                "ordering": ["nom"],
            },
        ),
    ]
