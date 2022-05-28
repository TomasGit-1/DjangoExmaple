from django.urls import path , include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path('dashboard' , views.dashboard , name = 'dashboard')

    # path('' , views.index , name = 'index'),
    # # path('code', views.PostListView.as_view()),
    # path('logout' , views.logout),
    # path('' , include("django.contrib.auth.urls")),
    # path('' , include("social_django.urls")),

    # path('dashboard' , views.dashboard , name = 'dashboard'),
    # # path('Clasificacion' , views.clasificacion , name ='Clasificacion'),
    # # path('User' , views.user, name ='User')
]