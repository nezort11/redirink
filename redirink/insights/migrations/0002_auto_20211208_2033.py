# Generated by Django 3.2.9 on 2021-12-08 20:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("insights", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Visitor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        db_index=True,
                        unique=True,
                        verbose_name="IP address of the visitor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Visitor",
                "verbose_name_plural": "Visitors",
            },
        ),
        migrations.AlterModelOptions(
            name="insight",
            options={
                "ordering": ["time"],
                "verbose_name": "Insight",
                "verbose_name_plural": "Insights",
            },
        ),
        migrations.RenameField(
            model_name="insight",
            old_name="visit_time",
            new_name="time",
        ),
        migrations.RemoveField(
            model_name="insight",
            name="ip_address",
        ),
        migrations.AddField(
            model_name="insight",
            name="visitor",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="insights",
                to="insights.visitor",
                verbose_name="Visitor",
            ),
        ),
    ]
