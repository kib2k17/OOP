from django import forms
from .models import Operator
class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ["employee_id","first_name","last_name","email","department","active"]
        widgets = {k: forms.TextInput(attrs={"class":"form-control"}) for k in ["employee_id","first_name","last_name","email"]}
