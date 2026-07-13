from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(verbose_name="Message")),
                ("type", models.CharField(choices=[("info", "Information"), ("alert", "Alerte"), ("success", "Succès")], default="info", max_length=20, verbose_name="Type")),
                ("is_read", models.BooleanField(default=False, verbose_name="Lu")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date de création")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="users.user", verbose_name="Utilisateur")),
            ],
            options={
                "db_table": "notifications",
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
                "ordering": ["-created_at"],
            },
        ),
    ]
