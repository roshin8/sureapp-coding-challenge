# Generated by Django 4.2.7 on 2023-11-10 08:15

from django.db import migrations, models
import insurance_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coverage_type', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=20)),
                ('has_pet', models.BooleanField()),
                ('coverage', models.JSONField(default=dict, validators=[insurance_app.validators.validate_json_keys_and_values])),
                ('pricing', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='StateConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=20, unique=True)),
                ('coverage_rate', models.JSONField(default=dict)),
                ('monthly_tax_rate', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
            ],
        ),
    ]
