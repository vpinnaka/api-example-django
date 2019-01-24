from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

import pytz


def get_object_first(classmodel):
    return classmodel.objects.first()


def parse_iso_date_string(date_str, timezone):
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    return date


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def update_or_create_object(classmodel, updated_values, **kwargs):
    return classmodel.objects.update_or_create(defaults=updated_values, **kwargs)


def get_today_date_time():
    pass
