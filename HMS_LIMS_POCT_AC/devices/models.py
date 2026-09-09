from django.db import models

class Device(models.Model):
    class Status(models.TextChoices):
        ACTIVE="ACTIVE","Active"; MAINTENANCE="MAINT","Maintenance"; OUT_OF_SERVICE="OOS","Out of Service"; RETIRED="RETIRED","Retired"
    device_id = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=120, blank=True)
    model = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    installation_date = models.DateField(null=True, blank=True)
    def __str__(self): return f"{self.device_id} - {self.device_type}"
    @property
    def is_available(self): return self.status == self.Status.ACTIVE
