from typing import Dict, Union
from decimal import Decimal
from .models import StateConfig, Quote
from django.core.exceptions import ObjectDoesNotExist

def get_state_config(state: str) -> Dict[str, Union[str, Decimal]]:
    try:
        state_config = StateConfig.objects.get(state=state)
        return {
            "state": state_config.state,
            "coverage_rate": state_config.coverage_rate,
            "monthly_tax_rate": state_config.monthly_tax_rate,
        }
    except ObjectDoesNotExist:
        return {}


def calculate_price(quote: Quote) -> Dict[str, Decimal]:
    state_config = get_state_config(quote.state)

    if not state_config:
        raise ValueError("Invalid state configuration")

    base_cost: Decimal = 20 if quote.coverage_type == "Basic" else 40
    pet_premium: Decimal = 20 if quote.has_pet else 0

    # Calculate base cost
    base_cost += pet_premium

    # Initialize total premium to 0
    total_premium: Decimal = 0

    # Check if there is a "coverage_rate" key in state_config
    if "coverage_rate" in state_config and isinstance(state_config["coverage_rate"], dict):
        coverage_rates: Dict[str, Decimal] = state_config["coverage_rate"]
        for key, coverage_rate in coverage_rates.items():
            if key.lower() in quote.coverage:
                total_premium += base_cost * coverage_rate

    # Calculate taxes
    tax_rate: Decimal = state_config.get("monthly_tax_rate", 0)
    taxes: Decimal = base_cost * tax_rate

    # Calculate total cost
    total_cost: Decimal = base_cost + taxes + total_premium

    return {
        "Monthly Subtotal": base_cost,
        "Monthly Taxes": taxes,
        "Monthly Total": total_cost,
    }
