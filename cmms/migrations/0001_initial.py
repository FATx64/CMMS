# Generated by Django 4.2.1 on 2023-06-23 12:23

import cmms.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                (
                    'email',
                    models.EmailField(error_messages={'unique': 'Email is already registered'}, max_length=254, unique=True),
                ),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('E', 'Engineer'), ('A', 'Admin')], max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=150)),
                ('repeat', models.IntegerField(default=0)),
                (
                    'repeat_frequency',
                    models.CharField(
                        blank=True,
                        choices=[('M', 'Monthly'), ('W', 'Weekly'), ('D', 'Daily'), ('N', 'Never')],
                        default='M',
                        max_length=5,
                        null=True,
                    ),
                ),
                ('expires_at', models.DateTimeField()),
                ('extra', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code', models.IntegerField()),
                ('location', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('tag', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('manufacture', models.CharField(max_length=150)),
                (
                    'pm_frequency',
                    models.CharField(
                        choices=[('M', 'Monthly'), ('W', 'Weekly'), ('D', 'Daily'), ('N', 'Never')],
                        default='M',
                        max_length=5,
                    ),
                ),
                ('cost', models.IntegerField()),
                ('picture', models.CharField(blank=True, default=cmms.utils.generate_hexa_id, max_length=32)),
                ('location', models.CharField(max_length=150)),
                ('installation_date', models.DateField()),
                ('warranty_date', models.DateField()),
                ('arrival_date', models.DateField()),
                ('note', models.CharField(blank=True, max_length=150)),
                (
                    'work_place',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmms.workplace'
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.BigIntegerField()),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, default='', max_length=150)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(blank=True, max_length=150)),
                ('work_hour', models.IntegerField()),
                ('avatar', models.CharField(blank=True, default=cmms.utils.generate_hexa_id, max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    'work_place',
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='cmms.workplace',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'type',
                    models.CharField(
                        choices=[('PM', 'Preventive Maintenance'), ('CM', 'Corrective Maintenance')], max_length=5
                    ),
                ),
                ('code', models.IntegerField()),
                ('description', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_complete', models.BooleanField(default=False)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmms.equipment')),
            ],
            options={
                'unique_together': {('type', 'code')},
            },
        ),
    ]
