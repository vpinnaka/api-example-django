from datetime import datetime
import pytz


def parse_iso_date_string(date_str, timezone):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
