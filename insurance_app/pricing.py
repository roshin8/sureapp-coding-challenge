from typing import Dict, Union
from decimal import Decimal
from .models import StateConfig, Quote
from .enums import CoverageType
from django.core.exceptions import ObjectDoesNotExist


def get_state_config(state: str) -> Dict[str, Union[str, float]]:
    """
    Retrieve the configuration for a specific state.

    Parameters:
    - state (str): The name of the state for which configuration is needed.

    Returns:
    Dict[str, Union[str, Decimal]]: A dictionary containing the state configuration with keys:
    - 'state': The name of the state.
    - 'coverage_rate': A dictionary representing coverage rates for different types.
    - 'monthly_tax_rate': The monthly tax rate for the state.

    If the state is not found, an empty dictionary is returned.

    Raises:
    ObjectDoesNotExist: If the state configuration is not found in the database.
    """

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
    """
    Calculate the pricing details for a given insurance quote.

    Parameters:
    - quote (Quote): The Quote instance for which pricing is calculated.

    Returns:
    Dict[str, float]: A dictionary containing pricing details with keys:
    - 'Monthly Subtotal': Monthly subtotal cost.
    - 'Monthly Taxes': Monthly taxes.
    - 'Monthly Total': Total monthly cost.

    Raises:
    ValueError: If the state configuration for the given quote is invalid.
    """

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
