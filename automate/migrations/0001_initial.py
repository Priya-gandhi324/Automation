# Generated by Django 4.0.5 on 2022-06-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_name', models.TextField()),
                ('scrape_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('till_date', models.DateField()),
                ('scrape_type', models.IntegerField()),
                ('orders', models.IntegerField()),
                ('judgements', models.IntegerField()),
            ],
        ),
    ]
