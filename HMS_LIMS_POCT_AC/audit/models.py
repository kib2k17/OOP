from django.conf import settings
from django.db import models
class AuditLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    action=models.CharField(max_length=100); entity_type=models.CharField(max_length=100,blank=True); entity_id=models.CharField(max_length=100,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True); details=models.TextField(blank=True)
    def __str__(self): return f"{self.timestamp} - {self.action}"
