from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AuditLog
@login_required
def audit_list(request): return render(request,"audit/list.html",{"logs":AuditLog.objects.select_related("user").all().order_by("-timestamp")[:500]})
