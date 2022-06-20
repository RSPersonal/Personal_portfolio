# Generated by Django 4.0.3 on 2022-05-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0014_propertymodel_property_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertymodel',
            name='status',
            field=models.CharField(choices=[('SD', 'Verkocht'), ('UO', 'Onder bod'), ('SWR', 'Verkocht onder voorbehoud'), ('NONE', 'Onbekend')], default='NONE', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='ask_price',
            field=models.IntegerField(default=0),
        ),
    ]