# Generated by Django 3.2.8 on 2021-10-12 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_fooditems_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='calorie',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fooditems',
            name='protein',
            field=models.FloatField(),
        ),
    ]
