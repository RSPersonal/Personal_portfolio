# Generated by Django 4.0.3 on 2022-05-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0002_alter_propertymodel_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertymodel',
            name='added_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='other_photos',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='thumbnail_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
