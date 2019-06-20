from django.contrib import admin
from .models import Visitor, Schedule, Profile, Visit, AllowedDevices


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'gender', 'category', 'blood_group', 'state', 'department', 'verified']
    list_editable = ['verified']
    list_filter = ['verified']

    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(Profile, ProfileAdmin)


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'gender', 'designation', 'email', 'profile_creation_time', 'address']


admin.site.register(Visitor, VisitorAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['visitor_id',
                    'requested_by',
                    'purpose',
                    'allowed_devices',
                    'in_time',
                    'out_time',
                    'allowed_days', 'approve', ]
    list_editable = ['approve']


admin.site.register(Schedule, ScheduleAdmin)

admin.site.register(AllowedDevices)


class VisitAdmin(admin.ModelAdmin):
    list_display = ['schedule_id', 'in_time', 'out_time', 'id_submitted']
    list_editable = ['id_submitted']


admin.site.register(Visit, VisitAdmin)
