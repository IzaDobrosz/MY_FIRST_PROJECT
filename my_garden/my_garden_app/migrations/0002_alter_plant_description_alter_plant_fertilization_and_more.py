# Generated by Django 4.2.11 on 2024-04-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_garden_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='fertilization',
            field=models.IntegerField(choices=[(1, 'Regular'), (2, 'Occasional')], verbose_name='Nawożenie'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='flowering_season',
            field=models.IntegerField(choices=[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'None')], verbose_name='Sezon kwitnienia'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='max_height',
            field=models.IntegerField(choices=[(1, 'Tall'), (2, 'Medium'), (3, 'Short')], verbose_name='Wysokość_max'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='pest_disease_resistance',
            field=models.IntegerField(choices=[(1, 'Odporny'), (2, 'Podatny')], verbose_name='Odporność na szkodniki i choroby'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='pruning_frequency',
            field=models.IntegerField(choices=[(1, 'Regularne'), (2, 'Okazjonalne')], verbose_name='Częstotliwość przycinania'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='spread',
            field=models.IntegerField(choices=[(1, 'Wide'), (2, 'Moderate'), (3, 'Compact')], verbose_name='Rozpiętość'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='sunlight_exposure',
            field=models.IntegerField(choices=[(1, 'Full Sun'), (2, 'Partial Shade'), (3, 'Shade')], verbose_name='Nasłonecznienie'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='watering_needs',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Moderate'), (3, 'High')], verbose_name='Podlewanie'),
        ),
    ]