from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pharmacie",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=255)),
                ("adresse", models.TextField()),
                ("commune", models.CharField(max_length=150)),
                ("telephone", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("horaire_ouverture", models.TimeField()),
                ("horaire_fermeture", models.TimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "pharmacies",
                "verbose_name": "Pharmacie",
                "verbose_name_plural": "Pharmacies",
            },
        ),
    ]
