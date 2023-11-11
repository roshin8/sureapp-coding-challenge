from typing import Dict, Union
from decimal import Decimal
from .models import StateConfig, Quote
from .enums import CoverageType
from django.core.exceptions import ObjectDoesNotExist


def get_state_config(state: str) -> Dict[str, Union[str, float]]:
    try:
        state_config = StateConfig.objects.get(state=state)
        return {
            "state": state_config.state,
            "coverage_rate": state_config.coverage_rate,
            "monthly_tax_rate": state_config.monthly_tax_rate,
        }
    except ObjectDoesNotExist:
        return {}


def calculate_price(quote: Quote) -> Dict[str, float]:
    state_config = get_state_config(quote.state)

    if not state_config:
        raise ValueError("Invalid state configuration")

    base_cost: float = 20.0 if quote.coverage_type == CoverageType.BASIC.value else 40.0
    pet_premium: float = 20.0 if quote.has_pet else 0.0

    # Calculate base cost
    base_cost += pet_premium

    # Initialize total premium to 0.0
    total_premium: float = 0.0

    # Handle multiple coverages like flood or hurricane without modifying code
    state_coverage_rates: Dict[str, Union[str, float]] = state_config["coverage_rate"]

    # Filter keys with True values in quote.coverage
    selected_coverages = {key: value for key, value in quote.coverage.items() if value}

    for key in selected_coverages:
        if key.lower() in state_coverage_rates:
            total_premium += base_cost * state_coverage_rates[key.lower()]

    # Calculate variables
    subtotal: float = base_cost + total_premium
    taxes: float = subtotal * state_config["monthly_tax_rate"]
    total_cost: float = subtotal + taxes 

    return {
        "Monthly Subtotal": float(str(subtotal)[:4]),
        "Monthly Taxes": float(str(taxes)[:4]),
        "Monthly Total": float(str(total_cost)[:5]),
    }
