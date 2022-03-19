# Generated by Django 4.0.2 on 2022-03-09 20:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_name', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=20)),
                ('buy_price', models.FloatField()),
                ('market', models.CharField(max_length=20)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_projects.portfolio')),
            ],
        ),
    ]