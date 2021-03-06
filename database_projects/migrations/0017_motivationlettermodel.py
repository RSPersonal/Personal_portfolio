# Generated by Django 4.0.3 on 2022-04-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_projects', '0016_portfolio_monthly_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivationLetterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter_body', models.TextField(default='')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('firm_name', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
