from django.conf import settings
from django.db import models
from devices.models import Device
from competency.models import TestMethod
class QualityControlRecord(models.Model):
    device=models.ForeignKey(Device,on_delete=models.PROTECT)
    test_method=models.ForeignKey(TestMethod,on_delete=models.PROTECT)
    control_level=models.CharField(max_length=50)
    lot_number=models.CharField(max_length=100)
    result=models.FloatField(); lower_limit=models.FloatField(); upper_limit=models.FloatField()
    performed_at=models.DateTimeField()
    performed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    corrective_action=models.TextField(blank=True)
    @property
    def status(self): return "PASS" if self.lower_limit <= self.result <= self.upper_limit else "FAIL"
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.lower_limit > self.upper_limit: raise ValidationError("Lower limit cannot exceed upper limit.")
