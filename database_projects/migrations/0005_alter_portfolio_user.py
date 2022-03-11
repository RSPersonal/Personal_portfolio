# Generated by Django 4.0.2 on 2022-03-11 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database_projects', '0004_portfolio_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
