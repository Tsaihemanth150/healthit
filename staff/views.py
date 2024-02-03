from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import generate_staff_id, Staff
from staff.forms import SignupForm


# Create your views here.

def register_staff_view(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST)

        if signupForm.is_valid():
            try:
                # Save the User instance
                user = signupForm.save(commit=False)
                user.set_password(signupForm.cleaned_data['password1'])
                user.save()

                # Create a Member instance and link it to the User
                member = Staff.objects.create(
                    user=user,
                    email=signupForm.cleaned_data['email'],
                    address='',  # Add address, mobile, nationality as needed
                    mobile='',
                    nationality=''
                )

                # Generate custom_id for the Member instance
                generate_staff_id(sender=Staff, instance=member)

                # Log the user in
                login(request, user)

                messages.success(request, 'Account created successfully. Send deatils of the staff.')
                return HttpResponseRedirect(reverse('admindashbord'))
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
