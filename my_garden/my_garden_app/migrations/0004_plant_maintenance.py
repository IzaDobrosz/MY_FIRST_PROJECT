# Generated by Django 4.2.11 on 2024-04-26 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_garden_app', '0003_alter_plant_fertilization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant_Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=120, verbose_name='Zadanie')),
                ('task_description', models.TextField(verbose_name='Opis')),
                ('week_of_month', models.IntegerField(choices=[(1, 'Pierwszy'), (2, 'Drugi'), (3, 'Trzeci'), (4, 'Czwarty'), (5, 'Ostatni')], verbose_name='Tydzień')),
                ('month', models.IntegerField(choices=[(1, 'Styczeń'), (2, 'Luty'), (3, 'Marzec'), (4, 'Kwiecień'), (5, 'Maj'), (6, 'Czerwiec'), (7, 'Lipiec'), (8, 'Sierpień'), (9, 'Wrzesień'), (10, 'Październik'), (11, 'Listopad'), (12, 'Grudzień')], verbose_name='Miesiąc')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_garden_app.plant', verbose_name='Nazwa')),
            ],
        ),
    ]