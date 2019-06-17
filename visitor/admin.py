from django.contrib import admin
from .models import Visitor, Schedule, Profile, Visit
# Register your models here.

admin.site.register(Visitor)
admin.site.register(Schedule)
admin.site.register(Profile)
admin.site.register(Visit)
