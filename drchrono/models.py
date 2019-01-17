from django.db import models
from django.utils import timezone
# Add your models here


class AppointmentSchedule(models.Model):
    patient = models.CharField(max_length=50)
    appointment_time = models.DateTimeField(default=timezone.now)
    appointment_status = models.CharField(max_length=50)
    checkedin_status = models.BooleanField(default=False)
    checkedin_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} appointment at {}'.format(self.patient, self.appointment_time)
