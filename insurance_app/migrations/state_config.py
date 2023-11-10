from django.db import migrations

def populate_state_config(apps, schema_editor):
    StateConfig = apps.get_model('insurance_app', 'StateConfig')

    state_config_data = [
        {
            'state': 'California',
            'coverage_rate': {"flood": 0.02},
            'monthly_tax_rate': 0.01,
        },
        {
            'state': 'Texas',
            'coverage_rate': {"flood": 0.5},
            'monthly_tax_rate': 0.005,
        },
        {
            'state': 'New York',
            'coverage_rate': {"flood": 0.1},
            'monthly_tax_rate': 0.02,
        },
        # Add more state configurations as needed
    ]

    for config in state_config_data:
        StateConfig.objects.create(**config)

class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_state_config),
    ]
