from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm
from . import models as CMODEL
from . import forms as CFORM
from staff import models as SMODEL
from .models import Member, generate_member_id
from django.core.exceptions import ObjectDoesNotExist



## Authentication ##################################################################
def signup_view(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST)

        if signupForm.is_valid():
            try:
                # Save the User instance
                user = signupForm.save(commit=False)
                user.set_password(signupForm.cleaned_data['password1'])
                user.save()

                # Create a Member instance and link it to the User
                member = Member.objects.create(
                    user=user,
                    email=signupForm.cleaned_data['email'],
                    address='',  # Add address, mobile, nationality as needed
                    mobile='',
                    nationality=''
                )

                # Generate custom_id for the Member instance
                generate_member_id(sender=Member, instance=member)

                # Log the user in
                login(request, user)

                messages.success(request, 'Account created successfully. You are now logged in.')
                return HttpResponseRedirect(reverse('home'))
            except ValidationError as e:
                # Print any validation error that may occur during save
                print(f"Validation Error: {e}")
                messages.error(request, 'Error creating account. Please try again.')
        else:
            # Print form errors for debugging
            print(signupForm.errors)
            messages.error(request, 'Invalid form submission. Please correct the errors.')

    else:
        signupForm = SignupForm()

    mydict = {'signupForm': signupForm}
    return render(request, 'member/signup.html', context=mydict)


def is_admin(user):  ### Check user is staff or not
    return user.is_staff


def is_staff(user):
    try:
        staff = SMODEL.Staff.objects.get(user=user)
        return staff.healthit_staff
    except ObjectDoesNotExist:
        return False

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        # Redirect to a different URL for authenticated users
        return redirect('home')  # Change 'home' to the desired URL

    # Continue with the default LoginView for non-authenticated users
    return LoginView.as_view(template_name='member/login.html')(request, *args, **kwargs)


def afterlogin_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            messages.success(request, 'Hello, welcome to ADMIN')
            return redirect('admindashboard')
        elif is_staff(request.user):
            return redirect('staff-profile')
        else:
            messages.success(request, 'Hello, welcome to Healthit!!!')
            return redirect('myprofile')

    # If user is not authenticated
    return redirect('login')  # Redirect to login page if not authenticated



################# Account or Profile Section ###########################################################

def member_profile_view(request):
    if request.user.is_authenticated:
        member_instance = Member.objects.get(user=request.user)

        context = {'member_instance': member_instance}
        return render(request, 'member/staff_profile.html', context)
    else:
        return redirect('home')


###### Admin Proflie ############################
@login_required(login_url='login')
def admin_dashboard_view(request):
    return render(request, 'admin/adminprofile.html')


@login_required(login_url='login')
def manage_members_view(request):
    dict = {
        'total_user': CMODEL.Member.objects.all().count(),
    }
    return render(request, 'admin/manage_members.html', context=dict)


@login_required(login_url='login')
def manage_staff_view(request):
    dict = {
        'total_user': SMODEL.Staff.objects.all().count(),
    }
    return render(request, 'admin/manage_staff.html', context=dict)


@login_required(login_url='login')
def admin_question_view(request):
    questions = CMODEL.Question.objects.all()
    return render(request, 'admin/admin_question.html', {'questions': questions})


@login_required(login_url='login')
def update_question_view(request, pk):
    question = CMODEL.Question.objects.get(id=pk)
    questionForm = CFORM.QuestionForm(instance=question)

    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST, instance=question)

        if questionForm.is_valid():
            admin_comment = request.POST.get('admin_comment')

            question = questionForm.save(commit=False)
            question.admin_comment = admin_comment
            question.save()

            return redirect('admin-question')
    return render(request, 'admin/update_question.html', {'questionForm': questionForm})


#### Member Profile Scetions. #####################################################################################################
def ask_question_view(request):
    member = CMODEL.Member.objects.get(user_id=request.user.id)
    questionForm = CFORM.QuestionForm()

    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.member = member  # Use the member instance, not the class
            question.save()
            return redirect('questionhistory')

    return render(request, 'member/ask_question.html', {'questionForm': questionForm, 'member': member})


def question_history_view(request):
    member = CMODEL.Member.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(member=member)
    return render(request, 'member/question_history.html', {'questions': questions, 'member': member})
