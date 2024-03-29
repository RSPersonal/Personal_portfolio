# Generated by Django 4.0.3 on 2022-08-21 07:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0026_remove_positions_portfolio_new_positions_portfolio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='id_for_chart',
            field=models.CharField(blank=True, max_length=36),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='id',
            field=models.UUIDField(default=uuid.UUID('26b258a8-a651-4f3a-acbc-2f378adc8bb6'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='id',
            field=models.UUIDField(default=uuid.UUID('480b6066-534a-4b93-8e6c-ff510ae6bafd'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
