from rest_framework.exceptions import ValidationError


def validate_percentile(value):
    try:
        int_val = int(value)
        if int_val < 0 or int_val > 100:
            raise ValidationError(f'percentile [{value}] is beyond 0-100')
        return True
    except ValueError:
        raise ValidationError(f'percentile [{value}] is not a number')
