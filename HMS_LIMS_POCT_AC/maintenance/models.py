from datetime import date, timedelta
from django.conf import settings
from django.db import models
from devices.models import Device
class MaintenanceRecord(models.Model):
    device=models.ForeignKey(Device,on_delete=models.CASCADE,related_name="maintenance_records")
    maintenance_type=models.CharField(max_length=120)
    performed_date=models.DateField(); performed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    description=models.TextField(blank=True); next_maintenance_date=models.DateField()
    @property
    def status(self):
        today=date.today()
        if today>self.next_maintenance_date:return "OVERDUE"
        if today>=self.next_maintenance_date-timedelta(days=30):return "DUE SOON"
        return "CURRENT"
