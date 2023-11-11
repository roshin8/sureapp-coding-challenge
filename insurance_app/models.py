from django.db import models
from .validators import validate_json_keys_and_values
from .enums import COVERAGE_TYPE_CHOICES

class Quote(models.Model):
    """
    Represents a quote for insurance coverage.

    Fields:
    - buyer_name (str): The name of the buyer that is requesting for quote
    - coverage_type (str): The type of coverage, either 'Basic' or 'Premium'.
    - state (str): The state for which the insurance quote is applicable.
    - has_pet (bool): Indicates whether the customer has a pet.
    - coverage (dict): A JSON field containing additional coverage details.
    - pricing (dict): A JSON field containing pricing details.

    Methods:
    - __str__: Returns a human-readable string representation of the quote.
    """
    buyer_name = models.CharField(max_length=255)
    coverage_type = models.CharField(max_length=10, choices=COVERAGE_TYPE_CHOICES)
    state = models.CharField(max_length=20)
    has_pet = models.BooleanField()
    coverage = models.JSONField(default=dict, validators=[validate_json_keys_and_values])
    pricing = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"ID: {self.pk} -- Buyer Name: {self.buyer_name} | Coverage Type: {self.coverage_type} | State: {self.state}"


class StateConfig(models.Model):
    """
    Represents the configuration for insurance in a specific state.

    Fields:
    - state (str): The name of the state.
    - coverage_rate (dict): A JSON field containing coverage rates for different types.
    - monthly_tax_rate (float): The monthly tax rate for the state.
    """
    state = models.CharField(max_length=20, unique=True)
    coverage_rate = models.JSONField(default=dict)  #TODO add decimal validator?
    monthly_tax_rate = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.state

    def save(self, *args, **kwargs):
        # Ensure 'flood' key is present in coverage_rate with a default value
        self.coverage_rate.setdefault('flood', 0.0)
        super().save(*args, **kwargs)
