# Generated by Django 4.0.3 on 2022-05-17 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0007_alter_propertymodel_other_photos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertymodel',
            name='ask_price',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
