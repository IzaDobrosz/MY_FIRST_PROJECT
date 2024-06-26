# Generated by Django 4.2.11 on 2024-04-23 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_garden_app', '0002_alter_plant_description_alter_plant_fertilization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='fertilization',
            field=models.IntegerField(choices=[(1, 'Regularne'), (2, 'Okazjonalne')], verbose_name='Nawożenie'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='flowering_season',
            field=models.IntegerField(choices=[(1, 'Wiosna'), (2, 'Lato'), (3, 'Jesień'), (4, 'Brak')], verbose_name='Sezon kwitnienia'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='max_height',
            field=models.IntegerField(choices=[(1, 'Wysoka'), (2, 'Średnia'), (3, 'Niska')], verbose_name='Wysokość_max'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='spread',
            field=models.IntegerField(choices=[(1, 'Szeroka'), (2, 'Średnia'), (3, 'Kompaktowa')], verbose_name='Rozpiętość'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='sunlight_exposure',
            field=models.IntegerField(choices=[(1, 'Pełne słońce'), (2, 'Częściowy cień'), (3, 'Cień')], verbose_name='Nasłonecznienie'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='watering_needs',
            field=models.IntegerField(choices=[(1, 'Niskie'), (2, 'Umiarkowane'), (3, 'Wysokie')], verbose_name='Potrzeba podlewania'),
        ),
    ]
