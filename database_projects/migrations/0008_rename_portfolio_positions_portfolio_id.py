# Generated by Django 4.0.2 on 2022-03-15 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0007_remove_positions_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='positions',
            old_name='portfolio',
            new_name='portfolio_id',
        ),
    ]
