# Generated by Django 4.0.3 on 2022-04-16 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_alter_visitorcount_visitor_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(default='', max_length=40)),
            ],
        ),
    ]
