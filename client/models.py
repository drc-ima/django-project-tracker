from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='clients')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'client'
        ordering = ['-created_at',]

