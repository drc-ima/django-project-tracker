from django.urls import path
from .views import *

app_name = 'client'

urlpatterns = [
    path('', Clients.as_view()),
    path('<id>/', ClientId.as_view()),
]