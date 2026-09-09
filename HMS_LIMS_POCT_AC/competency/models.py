from datetime import date, timedelta
from django.conf import settings
from django.db import models
from operators.models import Operator

class TestMethod(models.Model):
    name=models.CharField(max_length=150, unique=True)
    specimen_type=models.CharField(max_length=100, blank=True)
    device_type=models.CharField(max_length=120, blank=True)
    active=models.BooleanField(default=True)
    def __str__(self): return self.name

class Competency(models.Model):
    operator=models.ForeignKey(Operator,on_delete=models.CASCADE,related_name="competencies")
    test_method=models.ForeignKey(TestMethod,on_delete=models.PROTECT)
    assessor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    completion_date=models.DateField()
    expiration_date=models.DateField()
    comments=models.TextField(blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["operator","test_method","expiration_date"],name="unique_operator_test_expiration")]
    @property
    def status(self):
        today=date.today()
        if today>self.expiration_date: return "EXPIRED"
        if today>=self.expiration_date-timedelta(days=90): return "DUE SOON"
        return "CURRENT"
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.expiration_date and self.completion_date and self.expiration_date < self.completion_date:
            raise ValidationError("Expiration date cannot be before completion date.")
    def __str__(self): return f"{self.operator} - {self.test_method}"
