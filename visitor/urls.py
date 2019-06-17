from django.urls import path
from . import views

app_name = 'visitor'

urlpatterns = [
   path('register/', views.register, name='register'),
   path('dashboard/', views.dashboard, name='dashboard')
]
