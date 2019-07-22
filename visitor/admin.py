from django.contrib import admin
from .models import Visitor, Schedule, Profile, Visit, AllowedDevices
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VisitReport(resources.ModelResource):
    class Meta:
        model = Visit


class VisitReportAdmin(ImportExportModelAdmin):
    resource_class = VisitReport
    list_display = ['schedule_id', 'in_time', 'out_time', 'id_submitted']
    list_editable = ['id_submitted']
    list_per_page = 15
    list_filter = ['id_submitted', 'in_time']
    search_fields = ['schedule_id__visitor_id__name']


admin.site.register(Visit, VisitReportAdmin)


# Register your models here.

class ProfileReport(resources.ModelResource):
    class Meta:
        model = Profile
        exclude = ['photo']


class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileReport
    list_display = ['name', 'designation', 'gender', 'category', 'blood_group', 'state', 'department', 'verified']
    list_editable = ['verified']
    list_filter = ['verified']

    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(Profile, ProfileAdmin)


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'gender', 'designation', 'email', 'profile_creation_time', 'address']


admin.site.register(Visitor, VisitorAdmin)


class ScheduleReport(resources.ModelResource):
    class Meta:
        model = Schedule

    def dehydrate_requested_by(self, schedule):
        return '%s %s' % (schedule.requested_by.first_name, schedule.requested_by.last_name)

    def dehydrate_visitor_id(self, schedule):
        return '%s' % schedule.visitor_id.name


class ScheduleAdmin(ImportExportModelAdmin):
    resource_class = ScheduleReport
    list_display = ['visitor_id',
                    'requested_by',
                    'purpose',
                    'in_time',
                    'out_time',
                    'allowed_days', 'approve', ]
    list_editable = ['approve']
    list_filter = ['in_time', 'purpose', 'approve']
    list_per_page = 15
    search_fields = ['visitor_id__name']


admin.site.register(Schedule, ScheduleAdmin)

admin.site.register(AllowedDevices)
