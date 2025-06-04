from django.contrib import admin
from django.urls import path, include
from .views import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("doctors.doctors_urls")),
    path('', include("appointments.appointments_urls")),
    path('', include("users.users_urls")),
]
