from django.db import models
from django.utils import timezone
# Add your models here


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return '{} - {}, {} in {}'.format(
            self.id,
            self.first_name,
            self.last_name,
            self.timezone
        )


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    social_security_number = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    date_of_birth = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    cell_phone = models.CharField(max_length=25, null=True)

    def __str__(self):
        return '[ {},{} - {}, {}, {}]'.format(
            self.first_name,
            self.last_name,
            self.social_security_number,
            self.email,
            self.gender
        )


class Appointment(models.Model):
    STATUS_CHOICE = (
        ('current', 'Current'),
        ('past', 'Past'),
        ('future', 'Future')
    )
    id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=200, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_time = models.DateTimeField()
    appointment_status = models.CharField(max_length=50, null=True)
    duration = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()
    checkedin_status = models.BooleanField(default=False)
    checkedin_time = models.DateTimeField(null=True)
    waittime = models.IntegerField()
    exam_room = models.IntegerField()
    reason = models.CharField(max_length=200)
    queue_status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='future')

    class Meta:
        ordering = ('appointment_time',)

    def __str__(self):
        return '{} appointment at {}'.format(self.patient, self.appointment_time)
