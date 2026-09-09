from django import forms
from .models import MaintenanceRecord
class MaintenanceForm(forms.ModelForm):
    class Meta:
        model=MaintenanceRecord; fields="__all__"
        widgets={"performed_date":forms.DateInput(attrs={"type":"date","class":"form-control"}),"next_maintenance_date":forms.DateInput(attrs={"type":"date","class":"form-control"})}
