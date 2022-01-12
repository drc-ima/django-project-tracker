from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Create your models here.

TRACKING_TYPE = [
    ('M', 'Milestones'),
    # ('F', 'Features'),
    ('C', 'Checklist'),
    ('U', 'User Stories')
]


STATUS = [
    (0, 'Not Started'),
    (1, 'Started'),
    (2, 'Pending'),
    (3, 'On Hold'),
    (4, 'Canceled'),
    (5, 'Completed')
]


class Project(models.Model):
    client = models.ForeignKey("client.Client", on_delete=models.SET_NULL, blank=True, null=True, related_name="project_client")
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tracking_type = models.CharField(blank=True, null=True, max_length=255, choices=TRACKING_TYPE)
    status = models.IntegerField(default=0, choices=STATUS)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='projects')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'project'
        ordering = ['-created_at',]
    

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, related_name="milestone_project")
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='milestones')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "milestone"
        ordering = ['-created_at',]


class Feature(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, related_name='feature_milestone', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='feature_project', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='features')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "feature"
        ordering = ['-created_at',]


class CheckList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='checklist_project', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='checklists')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "checklist"
        ordering = ['-created_at',]
