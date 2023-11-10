from django.core.exceptions import ValidationError

def validate_json_keys_and_values(value):
    if not isinstance(value, dict):
        raise ValidationError('Enter a valid JSON object.')

    for key, val in value.items():
        if not isinstance(key, str):
            raise ValidationError('Keys must be strings.')
        if not isinstance(val, bool):
            raise ValidationError('Values must be booleans.')
