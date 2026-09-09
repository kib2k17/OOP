from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import QCForm
from .models import QualityControlRecord
@login_required
def qc_list(request): return render(request,"quality_control/list.html",{"records":QualityControlRecord.objects.select_related("device","test_method","performed_by").all().order_by("-performed_at")})
@login_required
def qc_create(request):
    form=QCForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("qc-list")
    return render(request,"generic_form.html",{"form":form,"title":"Enter Quality Control"})
