# Generated by Django 5.0.3 on 2024-03-12 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rollouts", "0003_alter_featureflag_proportion_and_more"),
    ]

    # BEGIN;
    # --
    # -- Create model FeatureExposure
    # --
    # CREATE TABLE "feature_exposures" ("exposure_id" integer NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "owner" integer NULL, "repo" integer NULL, "timestamp" timestamp with time zone NOT NULL, "feature_flag_id" varchar(200) NOT NULL, "feature_flag_variant_id" integer NOT NULL);
    # ALTER TABLE "feature_exposures" ADD CONSTRAINT "feature_exposures_feature_flag_id_628f8212_fk_feature_f" FOREIGN KEY ("feature_flag_id") REFERENCES "feature_flags" ("name") DEFERRABLE INITIALLY DEFERRED;
    # ALTER TABLE "feature_exposures" ADD CONSTRAINT "feature_exposures_feature_flag_variant_bfb854ff_fk_feature_f" FOREIGN KEY ("feature_flag_variant_id") REFERENCES "feature_flag_variants" ("variant_id") DEFERRABLE INITIALLY DEFERRED;
    # CREATE INDEX "feature_exposures_feature_flag_id_628f8212" ON "feature_exposures" ("feature_flag_id");
    # CREATE INDEX "feature_exposures_feature_flag_id_628f8212_like" ON "feature_exposures" ("feature_flag_id" varchar_pattern_ops);
    # CREATE INDEX "feature_exposures_feature_flag_variant_id_bfb854ff" ON "feature_exposures" ("feature_flag_variant_id");
    # COMMIT;

    operations = [
        migrations.CreateModel(
            name="FeatureExposure",
            fields=[
                ("exposure_id", models.AutoField(primary_key=True, serialize=False)),
                ("owner", models.IntegerField(blank=True, null=True)),
                ("repo", models.IntegerField(blank=True, null=True)),
                ("timestamp", models.DateTimeField()),
                (
                    "feature_flag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exposures",
                        to="rollouts.featureflag",
                    ),
                ),
                (
                    "feature_flag_variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exposures",
                        to="rollouts.featureflagvariant",
                    ),
                ),
            ],
            options={
                "db_table": "feature_exposures",
            },
        ),
    ]