# Generated by Django 4.0.2 on 2022-03-11 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0002_portfolio_created_on_positions'),
    ]

    operations = [
        migrations.AddField(
            model_name='positions',
            name='added_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
