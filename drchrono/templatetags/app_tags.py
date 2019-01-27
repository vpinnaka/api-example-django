from django import template
from drchrono.models import Appointment
from datetime import datetime

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


@register.assignment_tag
def get_no_of_appointments_today():
    date = datetime.now()
    appointments = Appointment.objects.filter(
        appointment_time__year=date.year,
        appointment_time__month=date.month,
        appointment_time__day=date.day,
    )
    return len(appointments)


@register.assignment_tag
def get_no_of_appointments_complete_today():
    date = datetime.now()
    appointments = Appointment.past.filter(
        appointment_status='Complete'
    )
    return len(appointments)


@register.assignment_tag
def get_no_of_appointments_noshow_today():
    date = datetime.now()
    appointments = Appointment.past.filter(
        appointment_status='No Show'
    )
    return len(appointments)


@register.assignment_tag
def get_avg_session_spent_with_patient():
    appointments = Appointment.past.exclude(
        session_start_time=None, session_complete_time=None)
    total_session_time, count = 0, 0
    for appointment in appointments:
        if appointment.session_complete_time and appointment.session_start_time:
            total_session_time += int((appointment.session_complete_time -
                                       appointment.session_start_time).total_seconds() // 60)
            count += 1
    return int(total_session_time//count) if total_session_time and count else 0
