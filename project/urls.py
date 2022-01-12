from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
    path('', Projects.as_view()),
    path('<id>/', ProjectId.as_view()),
    path('checklists/<id>/', Checklists.as_view()),
    path('milestones/<id>/', Milestones.as_view()),
    path('milestones/features/<id>/', MilestoneFeatures.as_view())
]