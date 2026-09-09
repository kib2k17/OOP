from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import MaintenanceForm
from .models import MaintenanceRecord
@login_required
def maintenance_list(request): return render(request,"maintenance/list.html",{"records":MaintenanceRecord.objects.select_related("device","performed_by").all().order_by("next_maintenance_date")})
@login_required
def maintenance_create(request):
    form=MaintenanceForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("maintenance-list")
    return render(request,"generic_form.html",{"form":form,"title":"Add Maintenance Record"})
