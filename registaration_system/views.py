from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
import re

from db_connect import appointments_collection, users_collection, doctors_collection
from appointments.views import convert_objectid


def home(request):
    return render(request, "main.html")
