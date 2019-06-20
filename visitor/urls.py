from django.urls import path
from . import views

app_name = 'visitor'

urlpatterns = [
    #user registration
    path('register/', views.register, name='register'),
    #dashboard hai ye
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
   # path('test/', views.test, name="test"),
    path('schedule/', views.schedule, name="schedule"),
    path('visitor/update/', views.update_visitor, name= "update_visitor"),
]
