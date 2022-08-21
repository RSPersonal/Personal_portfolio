# Generated by Django 4.0.3 on 2022-08-19 13:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0021_portfolio_uuid_positions_uuid_alter_portfolio_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6e342db9-125b-4c4a-a873-90f65b184978'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('37d4e3a5-79b4-4bc0-9d90-2d46c489ec94'), editable=False, unique=True),
        ),
    ]