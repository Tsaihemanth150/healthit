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
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),     ## add the urls of Admin
    path('', include('members.urls')),   ## add the urls of members app
    path('', include('staff.urls')),  ## add memebers of  staff app
    path('', include('doctors.urls')), ## add doctors of  staff app

    ##### webiste basic urls ###
    path('', views.index, name="home"),
    path('contactus', views.contactus, name="contcatus"),
    path('copy-rights',views.copyrights_views,name="copy-rights"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('options',views.options,name="options"),
]
