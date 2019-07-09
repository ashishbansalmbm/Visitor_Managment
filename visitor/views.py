from django.http import HttpResponse
from django.shortcuts import render, redirect

import base64

from django.core.files.base import ContentFile

from .forms import RegistrationForm, UpdateUserForm, UpdateProfileFormVerified, UpdateProfileFormNotVerified, \
    UpdateScheduleForm, UpdateVisitorForm, VisitorEntryForm
from .models import Schedule, Visitor, Visit


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


def view_profile(request):
    context = {'user': request.user, 'profile': request.user.profile}
    return render(request, 'user/profile.html', context)


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


def test(request):
    if request.method == 'POST':
        print("hello")
        name = request.POST['name']
        year = request.POST['year']
        print(name, year)

        return HttpResponse("hello")
    return render(request, 'home/test.html')


#
#   def visitor(request):
#

def schedule(request):
    if request.method == "POST":
        schedule_form = UpdateScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            flag = 1
            return render(request, 'user/schedule.html', {'flag': flag})
    else:
        schedule_form = UpdateScheduleForm()
    context = {'schedule_form': schedule_form}
    return render(request, 'user/schedule.html', context)


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


def filter_by_date(date):
    return Schedule.filter(in_time__year=date.year,
                           in_time__month=date.month,
                           in_time__day=date.day)


def guard_homepage(request):
    if request.method == 'POST':
        try:
            if request.POST['action']:
                input_id = request.POST["idnum"]
                phone_num = request.POST["phone"]
                profile = Visitor.objects.raw("select * from visitor_Visitor where phone = %s or id = %s",
                                              [phone_num, input_id])
                idn = profile[0].id
                schedul = Schedule.objects.raw(
                    'select * from visitor_Schedule where  approve=1 and visitor_id_id=%s and in_time > current_timestamp ',
                    [idn])
                visitor_form = VisitorEntryForm()
                context = {'visitor_form': visitor_form, 'profile': profile, 'schedul': schedul}
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

    # if request.POST['action'] == 'Snap':
    #     pic = request.POST["photo"];
    # if request.POST['action'] == 'Snap':
    #    pic = request.POST["photo"]
    #    image_data = base64.b64decode(pic[22:] + b'=' * (-len(pic[22:]) % 4))
    #    imagene = ContentFile(image_data, 'imagen1.png')
    #    profile = Visitor.objects.raw("select * from visitor_Visitor where phone = %s or id = %s",
    #                                  [phone_num, input_id])
    #    profile.photo = imagene
    #    profile.save()

    user = Schedule.objects.raw('select * from visitor_Schedule where approve=1 and in_time >current_timestamp')
    visitor = Visit.objects.raw('select * from visitor_Visit where in_time < current_timestamp and out_time = in_time')
    return render(request, 'home/guard_homepage.html', {'user': user, 'visitor': visitor})


# def (request):
#   if request.method == "POST":

def visitor_profile(request):
    visitor_form = VisitorEntryForm()
    context = {'visitor_form': visitor_form}
    return render(request, 'home/visitor_profile.html', context)


def dashboard(request):
    user = request.user.id
    upcoming_visitor = Schedule.objects.raw(
        'select * from visitor_Schedule where in_time >current_timestamp  and approve=1 and requested_by_id = %s',
        [user])
    context = {'user': user, 'profile': request.user.profile,
               'upcoming_visitor': upcoming_visitor}
    return render(request, 'home/dashboard.html', context)


def past_visitor(request):
    user = request.user.id
    past_visitors = Schedule.objects.raw(
        'select * from visitor_Schedule as s,visitor_Visitor as v where s.in_time < current_timestamp and  s.requested_by_id = %s and v.id=s.visitor_id_id',
        [user])
    return render(request, 'home/past_visitor.html', {'past_visitors': past_visitors})


# ef html_to_pdf_view(request):
#   paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#   html_string = render_to_string('home/pdf_template.html', {'paragraphs': paragraphs})

#   html = HTML(string=html_string)
#   html.write_pdf(target='/tmp/mypdf.pdf');

#   fs = FileSystemStorage('/tmp')
#   with fs.open('mypdf.pdf') as pdf:
#       response = HttpResponse(pdf, content_type='application/pdf')
#       response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#       return response
#   return response

def scan_qr(request):
    return render(request, 'user/scan.html')
