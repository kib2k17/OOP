from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Operator(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="operators")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"
    def __str__(self): return f"{self.employee_id} - {self.full_name}"
