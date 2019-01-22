from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from .models import Doctor, Appointment, Patient
from .forms import CheckinForm
from django.utils import timezone
from datetime import datetime
from utils import get_object_or_none
import pytz
import json
import settings

from drchrono.endpoints import (
    DoctorEndpoint,
    AppointmentEndpoint,
    PatientEndpoint,
    APIException)


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'login.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark
        magic will fetch it for us if we've already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get
        doctor details. If this succeeds, we've proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        self.request.session['access_token'] = access_token

        doctor_api = DoctorEndpoint(access_token)
        patient_api = PatientEndpoint(access_token)
        apppointment_api = AppointmentEndpoint(access_token)

        # Grab the first doctor from the list; normally this would be the whole
        # practice group, but your hackathon account probably only has one doctor in it.
        doctor = doctor_api.get_and_store_data()
        self.request.session['doctor'] = doctor.id
        # Get patients and appointments for the doctor and store it in the local DB
        patient_api.store_data(doctor=doctor)

        date = datetime.now(tz=pytz.timezone(
            doctor.timezone)).strftime('%Y-%m-%d')
        apppointment_api.store_data(doctor=doctor, date=date)

        return doctor

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs


class AppointmentsView(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'appointment_view.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AppointmentsView, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        # appointments = self.make_api_request()

        kwargs['appointments'] = Appointment.objects.all()
        return kwargs


class AppointmentListView(View):

    def get(self, request):
        if self.request.is_ajax() and self.request.GET.get('listtype') == 'current':
            current_appointment = Appointment.current.first()
            # print current_appointment
            response_data = None
            if current_appointment:
                response_data = current_appointment
            else:
                nextappointment = Appointment.future.first()
                if nextappointment:
                    nextappointment.queue_status = 'current'
                    nextappointment.save()
                    response_data = nextappointment
            context = {
                'appointment': response_data,
            }
            return render(request, 'appointment_current.html', context)

        else:
            # TODO: Add the logic to get the data from sessions for checkin appointments and update the data
            context = {
                'future': Appointment.future.all(),
                'past': Appointment.past.all(),
            }
            return render(request, 'appointment_list.html', context)

    def post(self, request):
        access_token = self.request.session['access_token']
        apppointment_api = AppointmentEndpoint(access_token)
        if self.request.is_ajax() and self.request.POST.get('updatetype') == 'current':
            appointment = Appointment.current.first()
            if appointment:
                appointment_id = appointment.id
                appointment_status = self.request.POST.get('status')

                updateddate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                data = {
                    'status': appointment_status,
                    'updated_at': updateddate
                }
                response = {}
                try:
                    response = apppointment_api.update(appointment_id, data)
                    appointment.appointment_status = appointment_status
                    appointment.queue_status = 'past'
                    appointment.save()
                except APIException:
                    return JsonResponse({"status": "false"}, status=500)
            return JsonResponse({"status": "true"})
        elif self.request.POST.has_key('appointment_id'):
            appointment_id = self.request.POST.get('appointment_id')
            appointment_status = self.request.POST.get('status')
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.appointment_status = appointment_status
            appointment.checkedin_time = datetime.now()
            appointment.save()
            # put the checkedin appointments in sessions
            checkedin_appointments = self.request.session.get(
                'checkedin_appointment', [])
            checkedin_appointments.append(appointment_id)
            self.request.session.get['checkedin_appointment'] = checkedin_appointments

            updateddate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data = {
                'status': appointment_status,
                'updated_at': updateddate
            }
            response = {}
            try:
                response = apppointment_api.update(appointment_id, data)
            except APIException:
                return JsonResponse({"status": "false"}, status=500)
            return JsonResponse({"response": response})


class CheckinView(FormView):
    template_name = 'checkin.html'
    form_class = CheckinForm
    success_url = '/checkin_success/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        dob = form.cleaned_data.get('date_of_birth')
        ssn = form.cleaned_data.get('social_security_number')

        patient = get_object_or_none(Patient,
                                     first_name=first_name,
                                     last_name=last_name,
                                     date_of_birth=str(dob)
                                     )
        if patient:
            access_token = self.request.session['access_token']
            apppointment_api = AppointmentEndpoint(access_token)
            appointments = Appointment.objects.filter(patient=patient.id)
            for appointment in appointments:
                appointment.appointment_status = 'Checked In'
                appointment.checkedin_status = True
                appointment.checkedin_time = datetime.now()
                checkedin_appointments = self.request.session.get(
                    'checkedin_appointment', [])
                checkedin_appointments.append(appointment.id)
                updateddate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                data = {
                    'status': 'Checked In',
                    'updated_at': updateddate
                }
                response = {}
                try:
                    response = apppointment_api.update(appointment.id, data)
                    appointment.save()
                    self.request.session['checkedin_appointment'] = checkedin_appointments
                except APIException:
                    context = {
                        'form': form,
                        'message': 'Trouble checking you in, Please consult a staff member',
                    }
                    return render(self.request, "checkin.html", context)

            return super(CheckinView, self).form_valid(form)

        context = {
            'form': form,
            'message': 'Patient not found',
        }
        return render(self.request, "checkin.html", context)


class CheckinSuccessView(TemplateView):
    """
    The checkin successful form.
    """
    template_name = 'checkin_success.html'

    def get_context_data(self, **kwargs):
        kwargs = super(CheckinSuccessView, self).get_context_data(**kwargs)

        kwargs['doctor'] = Doctor.objects.first()
        kwargs['checkedinno'] = len(
            Appointment.objects.filter(checkedin_status=True))
        return kwargs
