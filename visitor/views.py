from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

import base64
from django.utils import six
from django.core.files.base import ContentFile
from openpyxl.worksheet import page

from .forms import RegistrationForm, UpdateUserForm, UpdateProfileFormVerified, UpdateProfileFormNotVerified, \
    UpdateScheduleForm, UpdateVisitorForm, AllowedDevicesForm
from .models import Schedule, Visitor, Visit, AllowedDevices
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group,)
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            display = 1
            title = 'Thank You!!'
            message = 'Your registration was Successful Please Login to continue!!'
            context = {'display': display, 'message': message, 'title': title}
            return render(request, 'home/homepage.html', context)
        '''display = 1
        title = 'OOPS!!'
        message = 'THERE WAS AN ERROR!!
        context = {'display': display, 'message': message, 'title': title}'''
        return render(request, 'registration/registration_form.html', {'form': form})

    else:
        form = RegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required
def view_profile(request):
    context = {'user': request.user, 'profile': request.user.profile}
    return render(request, 'user/profile.html', context)


@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if request.user.profile.verified:
            profile_form = UpdateProfileFormVerified(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile_form = UpdateProfileFormNotVerified(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('visitor:view_profile')

    else:
        if request.user.profile.verified:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileFormVerified(instance=request.user.profile)
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileFormNotVerified(instance=request.user.profile)
    profile = request.user.profile
    user = request.user
    context = {'user_form': user_form, 'profile_form': profile_form, 'profile': profile, 'user': user}
    return render(request, 'user/update_profile.html', context)


@login_required
@group_required('Scientist')
def schedule(request):
    if request.method == "POST":
        schedule_form = UpdateScheduleForm(request.POST)
        if schedule_form.is_valid():
            form = schedule_form.save(commit=False)
            form.requested_by = request.user
            form.save()
            flag = 1
            return render(request, 'user/schedule.html', {'flag': flag})
    else:
        schedule_form = UpdateScheduleForm()

    context = {'schedule_form': schedule_form}
    return render(request, 'user/schedule.html', context)


@login_required
@group_required('Scientist')
def schedule_edit(request, sch_id):
    if request.method == "POST":
        schedule_form = UpdateScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule = Schedule.objects.get(id=sch_id)
            visitor = schedule_form.data['visitor_id']
            schedule.visitor_id = Visitor.objects.get(id=visitor)
            schedule.approve = False
            schedule.purpose = schedule_form.data['purpose']
            schedule.in_time = schedule_form.data['in_time']
            schedule.out_time = schedule_form.data['out_time']
            schedule.allowed_days = schedule_form.data['allowed_days']
            schedule.meeting_place = schedule_form.data['meeting_place']
            schedule.save()
            return redirect('visitor:my_schedules')
    else:
        schedule_form = UpdateScheduleForm(instance=Schedule.objects.get(pk=sch_id))
    allowed_devices = AllowedDevices.objects.filter(schedule_id=sch_id)
    context = {'schedule_form': schedule_form, 'allowed_devices': allowed_devices}
    return render(request, 'user/schedule.html', context)


@login_required
@group_required('Scientist')
def update_visitor(request):
    if request.method == "POST":
        update_form = UpdateVisitorForm(request.POST)
        if update_form.is_valid():
            update_form.save()
            flag = 1
            return render(request, 'user/update_visitor.html', {'flag': flag})
        else:
            return HttpResponse("<p>There is an error!</p>")
    else:
        update_form = UpdateVisitorForm()
    context = {'update_form': update_form}
    return render(request, 'user/update_visitor.html', context)


@login_required
def filter_by_date(date):
    return Schedule.filter(in_time__year=date.year,
                           in_time__month=date.month,
                           in_time__day=date.day)


@login_required
@group_required('Guard')
def guard_homepage(request):
    if request.method == 'POST':
        try:
            if request.POST['action']:

                if request.POST["idnum"]:
                    input_id = request.POST["idnum"]
                    profile = Visitor.objects.raw("select * from visitor_Visitor where id = %s",
                                                  [input_id])
                elif request.POST["phone"]:
                    phone_num = request.POST["phone"]
                    profile = Visitor.objects.raw("select * from visitor_Visitor where phone = %s ",
                                                  [phone_num])
                else:
                    input_id = request.POST["idnum"]
                    phone_num = request.POST["phone"]
                    profile = Visitor.objects.raw("select * from visitor_Visitor where phone = %s and id = %s",
                                                  [phone_num, input_id])
                idn = profile[0].id

                schedul = Schedule.objects.raw(
                    'select * from visitor_Schedule where  approve=1 and entry_prohibition=0 and visitor_id_id=%s and julianday(current_timestamp) - julianday(in_time) < allowed_days and date(in_time)<= CURRENT_DATE order by in_time desc',
                    [idn])
                temp = 0;
                if not schedul:
                    return HttpResponse('<p>You are not Scheduled for today!</p>'
                                        '<button onClick="javascript:history.go(-1)">Take me back</button>')
                context = {'profile': profile, 'schedule': schedul}
                return render(request, 'home/visitor_profile.html', context)

        except:
            if request.POST.get("photo"):
                pic = request.POST.get("photo")
                pk = request.POST.get('pk')
                format, imgstr = pic.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                profile = Visitor.objects.get(pk=pk)
                profile.photo = data
                profile.save()
                return render(request, 'home/visitor_profile.html')

    user = Schedule.objects.raw(
        'select * from visitor_Schedule where approve=1 and entry_prohibition=0 and julianday(current_timestamp) - julianday(in_time) < allowed_days and date(in_time)<= CURRENT_DATE  order by in_time desc')
    visitor = Visit.objects.raw(
        'select * from visitor_Visit where in_time < current_timestamp and out_time = in_time order by in_time desc')
    return render(request, 'home/guard_homepage.html', {'user': user, 'visitor': visitor})


@login_required
@group_required('Guard')
def visitor_profile(request, id):
    profile = Visitor.objects.raw("select * from visitor_Visitor where id = %s", [id])
    schedul = Schedule.objects.raw(
        'select * from visitor_Schedule where  approve=1 and entry_prohibition=0 and visitor_id_id=%s and julianday(current_timestamp) - julianday(in_time) < allowed_days and date(in_time)<= CURRENT_DATE order by in_time desc',
        [id])
    temp = 0;
    if not schedul:
        return HttpResponse('<p>You are not Scheduled for today!</p>'
                            '<button onClick="javascript:history.go(-1)">Take me back</button>')
    context = {'profile': profile, 'schedule': schedul}
    return render(request, 'home/visitor_profile.html', context)


@login_required
@group_required('Guard')
def visitor_profile_out(request, id):
    profile = Visitor.objects.raw("select * from visitor_Visitor where id = %s", [id])
    schedul = Schedule.objects.raw(
        'select * from visitor_Schedule where visitor_id_id=%s and out_time > current_timestamp ',
        [id])
    temp = 0;
    if not schedul:
        return HttpResponse('<p>You are not Scheduled for today!</p>'
                            '<button onClick="javascript:history.go(-1)">Take me back</button>')
    context = {'profile': profile, 'schedule': schedul}
    return render(request, 'home/visitor_profile.html', context)


@login_required
@group_required('Scientist')
def dashboard(request):
    user = request.user.id
    upcoming_visitor = Schedule.objects.raw(
        'select * from visitor_Schedule where out_time >current_timestamp  and approve=1 and entry_prohibition=0 and requested_by_id = %s',
        [user])
    context = {'user': user, 'profile': request.user.profile,
               'upcoming_visitor': upcoming_visitor}
    return render(request, 'home/dashboard.html', context)


@login_required
@group_required('Scientist')
def past_visitor(request):
    user = request.user.id
    past_visitors = Schedule.objects.raw(
        'select * from visitor_Schedule as s,visitor_Visitor as x,visitor_Visit as  v where v.in_time < current_timestamp and  s.requested_by_id = %s and s.id=v.schedule_id_id and s.approve = 1 and x.id = s.visitor_id_id',
        [user])
    page = request.GET.get('page', 1)
    paginator = Paginator(past_visitors, 3)
    try:
        past_visitr = paginator.page(page)
    except PageNotAnInteger:
        past_visitr = paginator.page(1)
    except EmptyPage:
        past_visitr = paginator.page(paginator.num_pages)

    return render(request, 'home/past_visitor.html', {'past_visitors': past_visitr})


@login_required
@group_required('Guard')
def scan_qr(request):
    if request.method == 'POST':
        id = request.POST.get('id');
    return render(request, 'user/scan.html')


@login_required
@group_required('Scientist')
def my_schedule(request):
    user = request.user.id
    my_schedule = Schedule.objects.raw(
        'Select * from visitor_schedule as s where s.requested_by_id=%s order by s.in_time desc ', [user])

    page = request.GET.get('page', 1)
    paginator = Paginator(my_schedule, 3)
    try:
        schedul = paginator.page(page)
    except PageNotAnInteger:
        schedul = paginator.page(1)
    except EmptyPage:
        schedul = paginator.page(paginator.num_pages)

    return render(request, 'home/my_schedule.html', {'my_schedule': schedul})


@login_required
@group_required('Guard')
def in_time_enter(request):
    if request.is_ajax():
        id = request.POST.get('id')
        instance = Visit.objects.create(schedule_id_id=id)
        return render(request, 'home/visitor_profile.html')


@login_required
@group_required('Guard')
def out_time_enter(request):
    if request.is_ajax():
        id = request.POST.get('id')
        instance = Visit.objects.raw(
            'select * from visitor_visit as v where v.schedule_id_id=%s order by in_time desc ', [id])
        data = instance[0]
        data.out_time = timezone.now()
        data.save()
        return render(request, 'home/visitor_profile.html')


@login_required
@group_required('Scientist')
def schedule_disapprove(request, id):
    if request.method == 'GET':
        schedule = Schedule.objects.get(id=id)
        if schedule.entry_prohibition:
            schedule.entry_prohibition = False
        else:
            schedule.entry_prohibition = True
        schedule.save()
        return redirect('visitor:my_schedules')


@login_required
@group_required('Scientist')
def allowed_devices(request):
    if request.method == "POST":
        allowed_form = AllowedDevicesForm(request.POST)
        if allowed_form.is_valid():
            allowed_form.save()
            flag = 1;
            return render(request, 'user/allowed_devices.html', {'flag': flag})
    else:
        allowed_form = AllowedDevicesForm()
    context = {'allowed_form': allowed_form}
    return render(request, 'user/allowed_devices.html', context)


@login_required
@group_required('Scientist')
def allowed_devices_update(request, id):
    if request.method == "POST":
        allowed_form = AllowedDevicesForm(request.POST)
        if allowed_form.is_valid():
            device = AllowedDevices.objects.get(id=id)
            schedule_id = device.schedule.id
            device.device = allowed_form.data['device']
            device.detail = allowed_form.data['detail']
            device.save()
            return redirect('/user/my/schedules/' + str(schedule_id))
    else:
        device = AllowedDevices.objects.get(id=id)
        allowed_form = AllowedDevicesForm(instance=device)
        context = {'allowed_form': allowed_form}
        return render(request, 'user/allowed_devices.html', context)


@login_required
@group_required('Scientist')
def allowed_devices_delete(request, id):
    if request.method == "GET":
        device = AllowedDevices.objects.get(id=id)
        schedule_id = device.schedule.id
        device.delete()
        return redirect('/user/my/schedules/' + str(schedule_id))
