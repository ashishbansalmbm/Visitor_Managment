from django.urls import path
from . import views

app_name = 'visitor'

urlpatterns = [
    # user registration
    path('register/', views.register, name='register'),
    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/past_visitor/', views.past_visitor, name="past_visitor"),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    # path('test/', views.test, name="test"),
    path('schedule/', views.schedule, name="schedule"),
    path('visitor/update/', views.update_visitor, name="update_visitor"),
    path('home/guard_homepage/', views.guard_homepage, name="guard_homepage"),
    path('home/guard_homepage/visitor_entry/', views.visitor_profile, name="visitor_profile")

]
