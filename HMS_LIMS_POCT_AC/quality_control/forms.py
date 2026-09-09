from django import forms
from .models import QualityControlRecord
class QCForm(forms.ModelForm):
    class Meta:
        model=QualityControlRecord; fields="__all__"
        widgets={"performed_at":forms.DateTimeInput(attrs={"type":"datetime-local","class":"form-control"})}
