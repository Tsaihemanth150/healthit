from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'healthit/index.html')

def aboutus(request):
    return render(request,'healthit/aboutus.html')

def contactus(request):
    return render(request,'healthit/contactus.html')
def options(request):
    return render(request,'healthit/options.html')
