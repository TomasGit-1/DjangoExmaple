from django.shortcuts import render , HttpResponse

def index(request):
    return HttpResponse("Hello wordl . You're at the index")

def dashboard(request):
    return render(request , "web/dashboard.html")




