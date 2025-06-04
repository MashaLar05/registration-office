from django.urls import path
from .views import all_appointments, appointment_detail, user_appointments, user_appointment_detail

urlpatterns = [
    path("appointments/", all_appointments, name="all_appointments"),
    path('appointments/<str:appointment_id>',
         appointment_detail, name='appointment_detail'),
    path('user_appointments/', user_appointments, name='user_appointments'),
    path('user_appointments/<str:appointment_id>/',
         user_appointment_detail, name='user_appointment_detail'),
]
