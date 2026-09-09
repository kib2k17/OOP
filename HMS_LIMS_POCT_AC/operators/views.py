from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OperatorForm
from .models import Operator

@login_required
def operator_list(request):
    q = request.GET.get("q", "").strip()
    qs = Operator.objects.select_related("department").order_by("last_name","first_name")
    if q:
        qs = qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q) | qs.filter(employee_id__icontains=q)
    return render(request, "operators/list.html", {"operators": qs, "q": q})

@login_required
def operator_create(request):
    form = OperatorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(); return redirect("operator-list")
    return render(request, "operators/form.html", {"form": form, "title":"Add Operator"})

@login_required
def operator_detail(request, pk):
    operator = get_object_or_404(Operator.objects.select_related("department"), pk=pk)
    return render(request, "operators/detail.html", {"operator": operator})
