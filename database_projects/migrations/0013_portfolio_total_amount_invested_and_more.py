# Generated by Django 4.0.3 on 2022-03-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0012_positions_amount_invested'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='total_amount_invested',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='total_profit',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='total_profit_percentage',
            field=models.FloatField(default=0.0),
        ),
    ]
