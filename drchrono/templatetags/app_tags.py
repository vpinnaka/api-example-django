from django import template
from drchrono.models import Appointment

register = template.Library()


@register.assignment_tag
def get_avg_wait_time():
    appointments = Appointment.past.exclude(
        checkedin_time=None, session_start_time=None)
    total_wait_time, count = 0, 0
    for appointment in appointments:
        if appointment.session_start_time and appointment.checkedin_time:
            total_wait_time += int((appointment.session_start_time -
                                    appointment.checkedin_time).total_seconds() // 60)
            count += 1
    return int(total_wait_time//count) if total_wait_time and count else 0
