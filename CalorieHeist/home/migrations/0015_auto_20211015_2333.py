# Generated by Django 3.2.8 on 2021-10-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20211013_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealnutrients',
            name='calorie',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='mealnutrients',
            name='fat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='mealnutrients',
            name='fiber',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='mealnutrients',
            name='protein',
            field=models.FloatField(default=0),
        ),
    ]