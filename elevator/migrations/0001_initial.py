# Generated by Django 4.2.3 on 2023-07-09 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('current_floor', models.IntegerField(default=0)),
                ('door_open', models.BooleanField(default=False)),
                ('is_operational', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Elevator',
                'verbose_name_plural': 'Elevators',
            },
        ),
        migrations.CreateModel(
            name='ElevatorSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('floors', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Elevator system',
                'verbose_name_plural': 'Elevator systems',
            },
        ),
        migrations.CreateModel(
            name='ElevatorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('current_floor', models.IntegerField()),
                ('requested_floor', models.IntegerField()),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator', to='elevator.elevator')),
            ],
            options={
                'verbose_name': 'Elevator request',
                'verbose_name_plural': 'Elevator requests',
            },
        ),
        migrations.AddField(
            model_name='elevator',
            name='elevator_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator_system', to='elevator.elevatorsystem'),
        ),
    ]
