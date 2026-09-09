from django import forms
from .models import Device
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = "__all__"
        widgets = {"installation_date": forms.DateInput(attrs={"type":"date","class":"form-control"})}
