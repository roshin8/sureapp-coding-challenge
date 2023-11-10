from django.db import models
from .validators import validate_json_keys_and_values


class Quote(models.Model):
    coverage_type = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    has_pet = models.BooleanField()
    coverage = models.JSONField(default=dict, validators=[validate_json_keys_and_values])
    pricing = models.JSONField(default=dict)


class StateConfig(models.Model):
    state = models.CharField(max_length=20, unique=True)
    coverage_rate = models.JSONField(default=dict)  #TODO add decimal validator?
    monthly_tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)

    def save(self, *args, **kwargs):
        # Ensure 'flood' key is present in coverage_rate with a default value
        self.coverage_rate.setdefault('flood', 0.0)
        super().save(*args, **kwargs)
