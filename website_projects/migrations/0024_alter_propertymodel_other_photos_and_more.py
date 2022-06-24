# Generated by Django 4.0.3 on 2022-06-22 18:45

import core.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0023_alter_propertymodel_rental_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertymodel',
            name='other_photos',
            field=models.FileField(blank=True, null=True, storage=core.storage_backends.PublicMediaStorage, upload_to=''),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='thumbnail_photo',
            field=models.FileField(blank=True, null=True, storage=core.storage_backends.PublicMediaStorage, upload_to=''),
        ),
    ]