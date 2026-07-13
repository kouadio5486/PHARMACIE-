from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(verbose_name="Message")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")),
                ("receiver", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages_recus", to="users.user", verbose_name="Destinataire")),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages_envoyes", to="users.user", verbose_name="Expéditeur")),
            ],
            options={
                "db_table": "chats",
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
                "ordering": ["-created_at"],
            },
        ),
    ]
