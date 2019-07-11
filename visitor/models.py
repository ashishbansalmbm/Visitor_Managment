from django.db import models
from enumerations.enum import UserType, BloodGroup, Gender, Category, DeviceType
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date
from django.utils import timezone


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    gender = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in Gender], default='')
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    contact = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='profile_photo', help_text='Your Photo name should be same as your name',
                              blank=True, null=True)
    category = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in Category],
                                default='')
    blood_group = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in BloodGroup],
                                   blank=True, null=True)
    designation = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in UserType], default='')
    verified = models.BooleanField(default=False)
    department = models.CharField(max_length=50)

    class Meta:
        permissions = (

        )

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


# Automatically Called Whenever an user instance is created
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile.objects.create(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Visitor(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in Gender], default='')
    designation = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    profile_creation_time = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='visitors', blank=True, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    visitor_id = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True)
    approve = models.BooleanField(default=False)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    allowed_devices = models.CharField(max_length=250, blank=True, null=True)
    in_time = models.DateTimeField(default=timezone.now)
    out_time = models.DateTimeField(default=timezone.now)
    allowed_days = models.PositiveIntegerField()
    meeting_place = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.visitor_id) + ' (In_time) ' + str(self.in_time.date()) + '  ' + str(
            self.in_time.time()) + ' (duration) ' \
               + str(self.allowed_days)


class Visit(models.Model):
    schedule_id = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    in_time = models.DateTimeField(default=timezone.now)
    out_time = models.DateTimeField(default=timezone.now)
    id_submitted = models.BooleanField(default=False)


class AllowedDevices(models.Model):
    visit_id = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    device = models.CharField(max_length=250)
    detail = models.TextField()
