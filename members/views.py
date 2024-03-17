from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from staff.models import generate_staff_id, Staff
from .forms import SignupForm, DepartmentForm, PlansForm, AssignMembersForm, EditProfileForm, RequestAppointmentForm
from . import models as CMODEL
from . import forms as CFORM
from staff import models as SMODEL
from .models import Member, generate_member_id,Department
from django.core.exceptions import ObjectDoesNotExist
from staff import  models as STMODEL
from .forms import AssignDepartmentForm

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

def is_admin_login(user):
    return user.is_authenticated and user.is_staff

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
            return redirect('admindashbord')
        elif is_staff(request.user):
            return redirect('staff-profile')
        else:
            messages.success(request, 'Hello, welcome to Healthit!!!')
            return redirect('member-dashboard')

    # If user is not authenticated
    return redirect('login')  # Redirect to login page if not authenticated



################# Account or Profile Section ###########################################################

def member_profile_view(request):
    if request.user.is_authenticated:
        member_instance = Member.objects.get(user=request.user)

        context = {'member_instance': member_instance}
        return render(request, 'member/myprofile.html', context)
    else:
        return redirect('home')



def view_total_members(request):
    members=Member.objects.all()
    return render(request,'admin/view_members.html',{'members': members})

###### Admin Proflie ############################
@login_required(login_url='login')
def admin_dashboard_view(request):
    return render(request, 'admin/adminprofile.html')


@login_required(login_url='login')
@user_passes_test(is_admin,login_url='/')
def manage_members_view(request):
    dict = {
        'total_user': CMODEL.Member.objects.all().count(),
    }
    return render(request, 'admin/manage_members.html', context=dict)

###### admin_staff #######################################
@login_required(login_url='login')
@user_passes_test(is_admin,login_url='/')
def manage_staff_view(request):
    dict = {
        'total_user': STMODEL.Staff.objects.all().count(),
    }
    return render(request, 'admin/manage_staff.html', context=dict)

def admin_view_staff(request):
    staff = STMODEL.Staff.objects.all()
    return render(request, 'admin/view_staff.html', {'staff': staff})

@user_passes_test(is_admin,login_url='/')
def register_staff_view(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST)

        if signupForm.is_valid():
            try:
                # Save the User instance
                user = signupForm.save(commit=False)
                user.set_password(signupForm.cleaned_data['password1'])
                user.save()

                # Create a Staff instance and link it to the User
                staff = Staff.objects.create(
                    user=user,
                    email=signupForm.cleaned_data['email'],
                    address='',  # Add address, mobile, nationality as needed
                    mobile='',
                    nationality='',

                )

                # Generate custom_id for the Staff instance
                generate_staff_id(sender=Staff, instance=staff)

                # No login is performed here

                messages.success(request, 'Account created successfully. Send details of the staff.')

                return HttpResponseRedirect(reverse_lazy('admindashbord'))

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
    return render(request, 'admin/register_staff.html', context=mydict)

def assign_member_view(request, custom_id):
    try:
        staff_member = STMODEL.Staff.objects.get(custom_id=custom_id)
    except STMODEL.Staff.DoesNotExist:
        # Handle the case where staff member with the given custom ID does not exist
        return render(request, 'staff_member_not_found.html')

    if request.method == 'POST':
        form = AssignMembersForm(request.POST)
        if form.is_valid():

            member_id = form.cleaned_data['Member']
            try:
                member = Member.objects.get(pk=member_id)
                staff_member.members.add(member)  # Use add() method to add member to staff
                return redirect('view-staff-with-member')  # Redirect to staff detail page
            except Member.DoesNotExist:
                # Handle the case where member with the given ID does not exist
                return render(request, 'member_not_found.html')
    else:
        form = AssignMembersForm()

    return render(request, 'admin/assign_member.html', {'form': form, 'staff_member': staff_member})

def delete_staff_view(request, custom_id):
    staff = STMODEL.Staff.objects.get(custom_id=custom_id)

    staff.user.delete()
    staff.delete()
    return redirect('view-staff')

@login_required(login_url='login')

def admin_question_view(request):
    questions = CMODEL.Question.objects.all()
    return render(request, 'admin/admin_question.html', {'questions': questions})


@login_required(login_url='login')

def update_admin_comment_view(request, pk):
    question = CMODEL.Question.objects.get(id=pk)

    if request.method == 'POST':
        # Retrieve the admin_comment value from the POST data
        admin_comment = request.POST.get('admin_comment')

        # Update the admin_comment field of the question object
        question.admin_comment = admin_comment

        # Save the updated question
        question.save()

        return redirect('admin-question')  # Redirect to the appropriate URL after updating

    # Render the form initially populated with existing admin comment
    return render(request, 'admin/update_question.html', {'questionForm': CFORM.QuestionForm(instance=question)})


#### Member Profile Scetions. #####################################################################################################

def view_member_dashboard(request):
    return render(request,'member/customer_dashboard.html')



def ask_question_view(request):
    member = Member.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)

        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.member = member
            question.save()
            return redirect('questionhistory')
        else:
            print(questionForm.errors)  # Print form errors for debugging
    else:
        questionForm =CFORM.QuestionForm()

    return render(request, 'member/ask_question.html', {'questionForm': questionForm, 'member': member})


def question_history_view(request):
    member = CMODEL.Member.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(member=member)
    return render(request, 'member/question_history.html', {'questions': questions, 'member': member})

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.member)
        if form.is_valid():
            form.save()
            # Redirect to a success page or reload the current page
            return redirect('myprofile')  # Assuming 'profile' is the URL name for viewing the profile
    else:
        form = EditProfileForm(instance=request.user.member)
    return render(request, 'member/edit_profile.html', {'form': form})




def Add_RequestAppointment(request):
    if request.method == 'POST':
        form = RequestAppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Create an appointment request object
                request_appointment = form.save(commit=False)
                # Associate the appointment request with the currently logged-in user
                request_appointment.member = request.user.member
                request_appointment.save()
                return redirect('view-appointment-request')  # Redirect to the appropriate view
            except Exception as e:
                # Handle the exception, maybe log it or render an error page
                print(e)
        else:
            print(form.errors)
    else:
        form = RequestAppointmentForm()
    return render(request, 'member/RequestAppointment.html', {'form': form})
def view_requested_appointments(request):
    member_id = request.user.id  # Assuming member_id is stored in the user object
    appointments = CMODEL.AppointmentRequset.objects.filter(member_id=member_id)
    return render(request, 'member/view_requsted_appointments.html', {'appointments': appointments})

### DEPARTMENT

def add_department_view(request):
    if request.method == 'POST':
        department_form = DepartmentForm(request.POST)

        if department_form.is_valid():
            try:
                department = department_form.save(commit=False)
                department.save()
                messages.success(request, 'Department added successfully.')
                return HttpResponseRedirect(reverse('department'))
            except Exception as e:
                print(f"Error adding department: {e}")
                messages.error(request, 'Error adding department. Please try again.')
        else:
            print(department_form.errors)
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        department_form = DepartmentForm()

    context = {'department_form': department_form}
    return render(request, 'admin/add_department.html', context)


### deapertment
@login_required(login_url='login')
@user_passes_test(is_admin,login_url='/')
def department_view(request):
    dict = {
        'total_member': CMODEL.Department.objects.all().count(),
    }
    return render(request, 'admin/department.html', context=dict)
@login_required(login_url='login')
def view_all_department_view(request):
    department = CMODEL.Department.objects.all()
    return render(request, 'admin/view_departments.html', {'department': department})

def delete_department_view(request, id):
    department = CMODEL.Department.objects.get(id=id)
    department.delete()
    return redirect('view-department')

## asign the departemnt

def assign_department_view(request, custom_id):
    try:
        staff_member = STMODEL.Staff.objects.get(custom_id=custom_id)
    except STMODEL.Staff.DoesNotExist:
        # Handle the case where staff member with the given custom ID does not exist
        return render(request, 'staff_member_not_found.html')

    if request.method == 'POST':
        form = AssignDepartmentForm(request.POST)
        if form.is_valid():
            department_id = form.cleaned_data['department']  # Get department ID from the form
            staff_member.department_id = department_id  # Assign department ID to staff member
            staff_member.save()
            return redirect('view-staff-with-department')  # Redirect to staff detail page
    else:
        form = AssignDepartmentForm()

    return render(request, 'admin/assign_department.html', {'form': form, 'staff_member': staff_member})

def view_staff_with_department(request):

    stf=STMODEL.Staff.objects.all()
    return render(request, 'admin/view_staff_with_department.html', {'stf':stf})

def view_staff_with_member(request):

    stf=STMODEL.Staff.objects.all()
    return render(request, 'admin/view_staff_with_member.html', {'stf':stf})

def view_members_with_staff_id(request,custom_id):
    stf = STMODEL.Staff.objects.get(custom_id=custom_id)
    return render(request, 'admin/view_members_with_staff_id.html', {'stf':stf})

### plans

@login_required(login_url='login')
def mange_plans_viwes(request):
    dict = {
        'ALl_Plans': CMODEL.Plan.objects.all().count(),
    }
    return render(request, 'admin/manage_plans.html', context=dict)

def view_plans_view(request):
    plans=CMODEL.Plan.objects.all()
    context = {'plans': plans}
    return render(request,'admin/view_plans.html',context)

def add_plans_view(request):
    if request.method == 'POST':
        plans_form = PlansForm(request.POST)

        if plans_form.is_valid():
            try:
                department = plans_form.save(commit=False)
                department.save()
                messages.success(request, 'Plan added successfully.')
                return HttpResponseRedirect(reverse('admindashbord'))
            except Exception as e:
                print(f"Error adding department: {e}")
                messages.error(request, 'Error adding department. Please try again.')
        else:
            print(plans_form.errors)
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        plans_form = PlansForm()

    context = {'plans_form': plans_form}
    return render(request, 'admin/add_palns.html', context)


############## PLANS ##############

def View_Plans_View(request):
    plan=CMODEL.Plan.objects.all()
    context = {'plan': plan}
    return render(request,'member/plans.html',context)