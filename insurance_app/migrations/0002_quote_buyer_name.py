# Generated by Django 4.2.7 on 2023-11-10 21:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0001_alter_stateconfig_monthly_tax_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='buyer_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
