"""
URL configuration for healthit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.contrib.auth.views import LogoutView,LoginView
from . import views

urlpatterns = [

#auth routes
    path('regiter-staff', views.register_staff_view, name='regiter-staff'),
    path('login/staff', views.custom_login, name='stafflogin'),


## Profile
    path('staff-profile',views.staff_profile_view,name='staff-profile'),
]
