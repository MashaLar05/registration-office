from django.urls import path
from .views import all_users, user_detail

urlpatterns = [
    path("users/", all_users, name="all_users"),
    path('users/<str:user_id>', user_detail, name='user_detail'),
]
