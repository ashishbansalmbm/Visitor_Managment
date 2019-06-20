from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UpdateUserForm, UpdateProfileFormVerified, UpdateProfileFormNotVerified, \
    UpdateScheduleForm, UpdateVisitorForm
from .models import Schedule


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


def dashboard(request):
    return render(request, 'home/dashboard.html')


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
        # print(user_form.errors.as_data())
        # print(profile_form.errors.as_data())
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
        user = Schedule.objects.raw
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
            return render(request, 'user/update_visitor.html', { 'flag': flag})
        else:
            return HttpResponse("<p>There is an error!</p>")
    else:
        update_form = UpdateVisitorForm()
    context = {'update_form': update_form}
    return render(request, 'user/update_visitor.html', context)
