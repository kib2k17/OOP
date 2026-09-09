from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import DeviceForm
from .models import Device
@login_required
def device_list(request): return render(request,"devices/list.html",{"devices":Device.objects.all().order_by("device_id")})
@login_required
def device_create(request):
    form=DeviceForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("device-list")
    return render(request,"generic_form.html",{"form":form,"title":"Add Device"})
