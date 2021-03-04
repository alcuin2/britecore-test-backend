from .models import RiskValueOptions
from dateutil.parser import parse


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def get_enum_values(obj):

    results = RiskValueOptions.objects.filter(risk_field=obj)
    return list(results)

