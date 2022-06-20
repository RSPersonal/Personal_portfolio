# Generated by Django 4.0.3 on 2022-06-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_projects', '0019_propertymodel_type_of_heating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertymodel',
            name='building_type',
            field=models.CharField(blank=True, choices=[('2-onder-1-kapwoning', '2-onder-1-kapwoning'), ('Eindwoning', 'Eindwoning'), ('Geschakelde woning', 'Geschakelde woning'), ('Hoekwoning', 'Hoekwoning'), ('Tussenwoning', 'Tussenwoning'), ('Vrijstaande woning', 'Vrijstaande woning'), ('Appartement', 'Appartement'), ('Onbekend', 'Onbekend')], default='Onbekend', max_length=20),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='status',
            field=models.CharField(blank=True, choices=[('Verkocht', 'Verkocht'), ('Onder bod', 'Onder bod'), ('Verkocht onder voorbehoud', 'Verkocht onder voorbehoud'), ('Beschikbaar', 'Beschikbaar'), ('Onbekend', 'Onbekend')], default='Onbekend', max_length=40),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='type_of_property',
            field=models.CharField(blank=True, choices=[('Koop', 'Koop'), ('Huur', 'Huur')], default='Koop', max_length=5),
        ),
    ]
