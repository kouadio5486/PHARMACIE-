from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacies", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ville",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=100, unique=True, verbose_name="Nom de la ville")),
                ("code", models.CharField(blank=True, max_length=20, unique=True, verbose_name="Code")),
                ("slug", models.SlugField(blank=True, max_length=120, unique=True, verbose_name="Slug")),
                ("district", models.CharField(blank=True, max_length=120, null=True, verbose_name="District")),
                ("region", models.CharField(blank=True, max_length=120, null=True, verbose_name="Région")),
                ("latitude", models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name="Latitude")),
                ("longitude", models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name="Longitude")),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "villes",
                "verbose_name": "Ville",
                "verbose_name_plural": "Villes",
                "ordering": ["nom"],
            },
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="ville",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="pharmacies", to="pharmacies.ville", verbose_name="Ville", null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="responsable",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pharmacies", to="users.user", verbose_name="Pharmacien responsable", null=True, blank=True, limit_choices_to={"role": "pharmacien"}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="is_pharmacie_de_garde",
            field=models.BooleanField(default=False, verbose_name="Pharmacie de garde"),
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="note_moyenne",
            field=models.FloatField(default=0.0, verbose_name="Note moyenne"),
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="pharmacies/", verbose_name="Image de la pharmacie"),
        ),
        migrations.AddField(
            model_name="pharmacie",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
    ]
