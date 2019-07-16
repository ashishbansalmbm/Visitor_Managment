from django.urls import path, re_path
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
    path('guard/', views.guard_homepage, name="guard_homepage"),
    path('home/guard_homepage/visitor_entry/<int:id>/', views.visitor_profile, name="visitor_profile"),
    path('home/guard_homepage/visitor_exit/<int:id>/', views.visitor_profile_out, name="visitor_profile_out"),
    path('scan/qr/', views.scan_qr, name="scan-qr"),
    path('my/schedules/', views.my_schedule, name='my_schedules'),
    re_path(r'^my/schedules/(?P<sch_id>\d+)/', views.schedule_edit, name='schedule_edit'),
    path('in/time/enter/', views.in_time_enter),
    path('out/time/enter/', views.out_time_enter),
    # re_path(r'^profile/(?P<pk>\d+)/' ,views.visitor_profile, name="visitor_profile"),
    # path('home/view/',views.html_to_pdf_view,name="html_to_pdf_view"),
]
