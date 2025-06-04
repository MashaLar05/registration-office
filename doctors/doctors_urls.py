from django.urls import path
from .views import all_doctors, doctor_detail

urlpatterns = [
    path("doctors/", all_doctors, name="all_doctors"),
    path('doctors/<str:doctors_id>', doctor_detail, name='doctor_detail'),
]
