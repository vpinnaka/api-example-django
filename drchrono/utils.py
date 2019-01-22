from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import pytz


def parse_iso_date_string(date_str, timezone):
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    # date = date.replace(tzinfo=timezone)
    return date


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
