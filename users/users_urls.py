from django.urls import path
from .views import all_users, user_detail, login_view, logout_view, index, user_profile, register_view, create_appointment

urlpatterns = [
    path('', index, name='index'),
    path('users/', all_users, name='all_users'),
    path('users/<str:user_id>/', user_detail, name='user_detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user_page/<str:user_id>/', user_profile, name='user_profile'),
    path('create_appointment/', create_appointment, name='create_appointment'),
]
