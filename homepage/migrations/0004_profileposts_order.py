# Generated by Django 4.0.2 on 2022-03-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_alter_profileposts_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileposts',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]