from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacies", "0002_add_ville_and_update_pharmacie"),
    ]

    operations = [
        migrations.AddField(
            model_name="pharmacie",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
