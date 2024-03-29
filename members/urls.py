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
    path('signup', views.signup_view, name='singup'),
    path('login/member', views.custom_login, name='login'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='componets/logout.html'),name='logout'),

## Admin Account or Profile routes Section
    path('myprofile', views.member_profile_view, name='myprofile'),
    path('admindashbord',views.admin_dashboard_view,name='admindashbord'),
    path('managemembers',views.manage_members_view,name='managemembers'),
    path('managestaff',views.manage_staff_view,name='managestaff'),

    #members
    path('view-members',views.view_total_members,name='view-members'),
    #questions
    path('admin-question',views.admin_question_view,name='admin-question'),
    path('update-question/<int:pk>', views.update_admin_comment_view,name='update-question'),

    #Department
    path('department',views.department_view,name='department'),
    path('view-department',views.view_all_department_view,name='view-department'),
    path('delete-department/<int:id>',views.delete_department_view,name='delete-department'),
    path('add-department',views.add_department_view,name='add-department'),
    path('assign-department/<str:custom_id>/', views.assign_department_view, name='assign-department'),
    path('view-staff-with-department',views.view_staff_with_department,name='view-staff-with-department'),

    ## staff
    path('view-staff', views.admin_view_staff, name='view-staff'),
    path('assign-member/<str:custom_id>/', views.assign_member_view, name='assign-member'),
    path('delete-staff/<str:custom_id>', views.delete_staff_view, name='delete-staff'),
    path('regiter-staff', views.register_staff_view, name='regiter-staff'),
    path('view-staff-with-member',views.view_staff_with_member,name='view-staff-with-member'),
    path('view-members-with-staff-id/<str:custom_id>',views.view_members_with_staff_id,name='view-members-with-staff-id'),
    #palns
    path('manage-plans',views.mange_plans_viwes,name='manage-plans'),
    path('view-plans',views.view_plans_view,name='view-plans'),
    path('add-plans',views.add_plans_view,name='add-plans'),

## Member Account or Profile Routes sections
    path('member-dashboard',views.view_member_dashboard,name='member-dashboard'),
    path('askquestion',views.ask_question_view,name='askquestion'),
    path('questionhistory',views.question_history_view,name='questionhistory'),
    path('plans',views.View_Plans_View,name='plans'),
    path('edit-profile',views.edit_profile,name='edit-profile'),
    path('add-appointment-request', views.Add_RequestAppointment, name='add-appointment-request'),
    path('view-appointment-request', views.view_requested_appointments, name='view-appointment-request'),
]
