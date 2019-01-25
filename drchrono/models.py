from django.db import models
from django.utils import timezone
from datetime import datetime
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

    def get_age(self):
        dob = datetime.strptime(self.date_of_birth, '%Y-%m-%d')
        today = datetime.today()
        return today.year - dob.year


class CurrentAppointmentManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return super(CurrentAppointmentManager, self).get_queryset()\
            .filter(
                appointment_time__year=date.year,
                appointment_time__month=date.month,
                appointment_time__day=date.day,
                queue_status='current',
        )


class FutureAppointmentManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return super(FutureAppointmentManager, self).get_queryset()\
            .filter(
                appointment_time__year=date.year,
                appointment_time__month=date.month,
                appointment_time__day=date.day,
                queue_status='future',
        )


class PastAppointmentManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return super(PastAppointmentManager, self).get_queryset()\
            .filter(
                appointment_time__year=date.year,
                appointment_time__month=date.month,
                appointment_time__day=date.day,
                queue_status='past',
        )


class TodayAppointmentManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return super(TodayAppointmentManager, self).get_queryset()\
            .filter(
                appointment_time__year=date.year,
                appointment_time__month=date.month,
                appointment_time__day=date.day,
        )


class Appointment(models.Model):
    objects = models.Manager()  # The default manger
    today = TodayAppointmentManager()
    current = CurrentAppointmentManager()
    future = FutureAppointmentManager()
    past = PastAppointmentManager()

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
    checkedin_status = models.BooleanField(default=False)
    checkedin_time = models.DateTimeField(null=True)
    session_start_time = models.DateTimeField(null=True)
    session_complete_time = models.DateTimeField(null=True)
    exam_room = models.IntegerField()
    reason = models.CharField(max_length=200, null=True)
    queue_status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='future')

    class Meta:
        ordering = ('appointment_time',)

    def __str__(self):
        return '{} appointment at {}'.format(self.patient, self.appointment_time)

    def get_wait_time(self):
        if self.checkedin_time and self.checkedin_status:
            return int((self.session_start_time - self.checkedin_time).total_seconds() // 60)
        return 0

    def get_time_left(self):
        time_elapsed = int(
            (datetime.now() - self.session_start_time).total_seconds() // 60)
        return self.duration - time_elapsed
