# Generated by Django 3.2.5 on 2021-07-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350)),
                ('completed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
