# Generated by Django 4.0.3 on 2022-05-22 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0011_propertymodel_temp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertymodel',
            name='temp_id',
        ),
    ]
