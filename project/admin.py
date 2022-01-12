from django.contrib import admin

from project.models import CheckList, Feature, Milestone, Project

# Register your models here.

admin.site.register(Project)
admin.site.register(CheckList)
admin.site.register(Milestone)
admin.site.register(Feature)