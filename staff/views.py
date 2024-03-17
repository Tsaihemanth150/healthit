from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import generate_staff_id, Staff
from staff.forms import SignupForm, ScheduleBlockForm
from django.urls import reverse_lazy
# Create your views here.




def is_staff(user):
    try:
        staff = Staff.objects.get(user=user)
        return staff.healthit_staff
    except ObjectDoesNotExist:
        return False

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        # Redirect to a different URL for authenticated users
        return redirect('home')  # Change 'home' to the desired URL

    # Continue with the default LoginView for non-authenticated users
    return LoginView.as_view(template_name='staff/login.html')(request, *args, **kwargs)


def staff_profile_view(request):
    if request.user.is_authenticated:
        staff = Staff.objects.get(user=request.user)

        context = {'staff': staff}
        return render(request, 'staff/staff_profile.html', context)
    else:
        return redirect('home')


@user_passes_test(is_staff, login_url='/')
def view_my_members(request):
    staff_members = Staff.objects.all()
    members = []
    for staff_member in staff_members:
        members.extend(staff_member.members.all())
    return render(request, 'staff/mymembers.html', {'members': members})


@user_passes_test(is_staff, login_url='/')
def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleBlockForm(request.POST)
        if form.is_valid():
            schedule_block = form.save(commit=False)
            schedule_block.staff = request.user.staff  # Assuming user's staff instance is linked
            schedule_block.save()
            return redirect('view_schedule')  # Redirect to a view to display all schedules
    else:
        form = ScheduleBlockForm()
    return render(request, 'staff/add_appointmnet.html', {'form': form})
