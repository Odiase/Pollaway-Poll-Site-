from django.urls import path
from .views import Login,sign_up,Logout,home_page

urlpatterns = [
    path("",home_page,name = "home"),
    path("sign-up/",sign_up,name = "sign-up"),
    path("login/", Login, name = "login"),
    path("logout/",Logout,name ="logout"),
]