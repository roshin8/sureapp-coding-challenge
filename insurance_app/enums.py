from enum import Enum

class CoverageType(Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"

COVERAGE_TYPE_CHOICES = [
    (CoverageType.BASIC.value, 'Basic'),
    (CoverageType.PREMIUM.value, 'Premium'),
]
