from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import InventoryForm
from .models import InventoryItem
@login_required
def inventory_list(request): return render(request,"inventory/list.html",{"items":InventoryItem.objects.all().order_by("expiration_date")})
@login_required
def inventory_create(request):
    form=InventoryForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("inventory-list")
    return render(request,"generic_form.html",{"form":form,"title":"Add Inventory Item"})
