import views
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', views.SetupView.as_view(), name='setup'),
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='welcome'),
    url(r'^checkin/$', views.CheckinView.as_view(), name='checkin'),
    url(r'^checkin_success/$', views.CheckinSuccessView.as_view(),
        name='checkin_success'),
    url(r'^appointments/$', views.AppointmentsView.as_view(), name='appointments'),
    url(r'^appointments_list/$', views.AppointmentListView.as_view(),
        name='appointment_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
