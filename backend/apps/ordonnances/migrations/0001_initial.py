from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Ordonnance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fichier", models.FileField(upload_to="ordonnances/", verbose_name="Fichier ordonnance")),
                ("statut", models.CharField(choices=[("en_attente", "En attente"), ("validee", "Validée"), ("refusee", "Refusée")], default="en_attente", max_length=20, verbose_name="Statut")),
                ("commentaire", models.TextField(blank=True, null=True, verbose_name="Commentaire")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ordonnances", to="users.user", verbose_name="Utilisateur")),
            ],
            options={
                "db_table": "ordonnances",
                "verbose_name": "Ordonnance",
                "verbose_name_plural": "Ordonnances",
                "ordering": ["-created_at"],
            },
        ),
    ]
