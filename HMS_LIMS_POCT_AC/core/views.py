from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from operators.models import Operator
from devices.models import Device
from competency.models import Competency
from quality_control.models import QualityControlRecord
from maintenance.models import MaintenanceRecord
from inventory.models import InventoryItem

@login_required
def dashboard(request):
    context = {
        "active_operators": Operator.objects.filter(active=True).count(),
        "active_devices": Device.objects.filter(status=Device.Status.ACTIVE).count(),
        "current_competencies": sum(1 for c in Competency.objects.all() if c.status == "CURRENT"),
        "due_competencies": sum(1 for c in Competency.objects.all() if c.status == "DUE SOON"),
        "expired_competencies": sum(1 for c in Competency.objects.all() if c.status == "EXPIRED"),
        "failed_qc": sum(1 for q in QualityControlRecord.objects.all() if q.status == "FAIL"),
        "maintenance_due": sum(1 for m in MaintenanceRecord.objects.all() if m.status in {"DUE SOON", "OVERDUE"}),
        "low_stock": sum(1 for i in InventoryItem.objects.all() if i.is_low_stock),
        "expired_inventory": sum(1 for i in InventoryItem.objects.all() if i.is_expired),
    }
    return render(request, "dashboard.html", context)
