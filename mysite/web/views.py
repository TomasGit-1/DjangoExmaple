# 📁 webappexample/views.py -----

import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponseRedirect ,HttpResponse

from .Folderclass.sendEmail import Gmail_API
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def index(request):
    return render(
        request,
        "web/index.html",
    )

def dashboard(request):
    return render(
        request,
        "web/dashboard.html"
    )

def email(request):
    return render(
        request,
        "web/Email.html"
    )


def send_mail_rute(request):
    try:
        if request.method == 'POST':
            data = request.POST.dict()
            objEmail = Gmail_API()
            # objEmail.gmail_create_draft([1,2,3])
            objEmail.gmail_send_message()
            results = {'val1' : 'this is x', 'val2' : True}
            return HttpResponse(json.dumps(results))
    except  Exception as e:
        return e


# from django.shortcuts import render, redirect
# from django.views.generic import View
# from django.utils.decorators import method_decorator
# # from .models import Post
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout as log_out
# from urllib.parse import urlencode
# from django.conf import settings
# from django.http import HttpResponseRedirect


# def index(request):
#     user = request.user
#     if user.is_authenticated:
#         return redirect("/dashboard")
#     else:
#         return render(request, "web/index.html")


# def logout(request):
#     log_out(request)

#     return_to = urlencode({"returnTo" : request.build_absolute_uri("/")})
#     logout_url = "https://{}/v2/logout?client_id={}&{}".format(
#         settings.AUTH0_DOMAIN, settings.AUTH0_CLIENT_ID , return_to
#     )
#     return HttpResponseRedirect(logout_url)


# # class PostListView(View):
# #     @method_decorator(login_required)
# #     def dispatch(self , *args , **kwargs):
# #         return super (PostListView , self).dispatch(*args , **kwargs)

# #     def get(self , request):
# #         post = Post.objects.all()
# #         context = {"posts" : post}
# #         return render(request,"home.html" , context)

# # def index(request):
# #     return HttpResponse("Hello wordl . You're at the index")
# @login_required
# def dashboard(request):
#     return render(request , "web/dashboard.html")

# # def clasificacion(request):
# #     return render(request , "web/clasificacion.html")

# # def user(request):
# #     return render(request , "web/Vuser.html")