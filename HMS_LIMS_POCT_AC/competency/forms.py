from django import forms
from .models import Competency, TestMethod
class CompetencyForm(forms.ModelForm):
    class Meta:
        model=Competency; fields="__all__"
        widgets={"completion_date":forms.DateInput(attrs={"type":"date","class":"form-control"}),"expiration_date":forms.DateInput(attrs={"type":"date","class":"form-control"})}
class TestMethodForm(forms.ModelForm):
    class Meta: model=TestMethod; fields="__all__"
