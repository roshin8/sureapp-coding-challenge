from django.db import models
from .validators import validate_json_keys_and_values
from .enums import COVERAGE_TYPE_CHOICES

class Quote(models.Model):
    buyer_name = models.CharField(max_length=255)
    coverage_type = models.CharField(max_length=10, choices=COVERAGE_TYPE_CHOICES)
    state = models.CharField(max_length=20)
    has_pet = models.BooleanField()
    coverage = models.JSONField(default=dict, validators=[validate_json_keys_and_values])
    pricing = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"ID: {self.pk} -- Buyer Name: {self.buyer_name} | Coverage Type: {self.coverage_type} | State: {self.state}"


class StateConfig(models.Model):
    state = models.CharField(max_length=20, unique=True)
    coverage_rate = models.JSONField(default=dict)  #TODO add decimal validator?
    monthly_tax_rate = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.state

    def save(self, *args, **kwargs):
        # Ensure 'flood' key is present in coverage_rate with a default value
        self.coverage_rate.setdefault('flood', 0.0)
        super().save(*args, **kwargs)
