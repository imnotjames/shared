# Generated by Django 4.2.11 on 2024-04-12 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0016_testresultreporttotals_error"),
    ]

    operations = [
        migrations.AddField(
            model_name="testinstance",
            name="flaky_status",
            field=models.CharField(
                choices=[
                    ("failed_in_default_branch", "Failed In Default Branch"),
                    ("consecutive_diff_outcomes", "Consecutive Diff Outcomes"),
                    ("unrelated_matching_failures", "Unrelated Matching Failures"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]