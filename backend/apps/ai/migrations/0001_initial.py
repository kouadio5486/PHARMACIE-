from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AIInteraction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("input", models.TextField(verbose_name="Entrée utilisateur")),
                ("output", models.TextField(verbose_name="Réponse du système")),
                ("type", models.CharField(choices=[("search", "Recherche médicament"), ("symptom", "Recherche par symptôme"), ("general", "Question générale")], default="general", max_length=20, verbose_name="Type de recherche")),
                ("context", models.JSONField(blank=True, default=dict, verbose_name="Contexte de recherche")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_interactions", to="users.user", verbose_name="Utilisateur")),
            ],
            options={
                "db_table": "ai_interactions",
                "verbose_name": "Interaction IA",
                "verbose_name_plural": "Interactions IA",
                "ordering": ["-created_at"],
            },
        ),
    ]
