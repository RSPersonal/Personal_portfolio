# Generated by Django 4.0.3 on 2022-06-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0020_alter_propertymodel_building_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertymodel',
            name='rental_price',
            field=models.IntegerField(default=0),
        ),
    ]
