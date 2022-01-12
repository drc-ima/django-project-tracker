from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path("signup/", Signup.as_view()),
    path("login/", Login.as_view()),
]
