from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CompetencyForm, TestMethodForm
from .models import Competency, TestMethod
@login_required
def competency_list(request): return render(request,"competency/list.html",{"competencies":Competency.objects.select_related("operator","test_method","assessor").all()})
@login_required
def competency_create(request):
    form=CompetencyForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("competency-list")
    return render(request,"generic_form.html",{"form":form,"title":"Record Competency"})
@login_required
def testmethod_list(request): return render(request,"competency/testmethods.html",{"tests":TestMethod.objects.all()})
@login_required
def testmethod_create(request):
    form=TestMethodForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); return redirect("testmethod-list")
    return render(request,"generic_form.html",{"form":form,"title":"Add Test Method"})
