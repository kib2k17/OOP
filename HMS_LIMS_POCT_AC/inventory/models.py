from datetime import date, timedelta
from django.db import models
class InventoryItem(models.Model):
    class Category(models.TextChoices):
        REAGENT="REAGENT","Reagent"; CONTROL="CONTROL","Control"; CARTRIDGE="CARTRIDGE","Cartridge"; STRIP="STRIP","Test Strip"; CONSUMABLE="CONSUMABLE","Consumable"
    item_name=models.CharField(max_length=150); category=models.CharField(max_length=20,choices=Category.choices)
    manufacturer=models.CharField(max_length=120,blank=True); lot_number=models.CharField(max_length=100)
    expiration_date=models.DateField(); quantity=models.PositiveIntegerField(); minimum_quantity=models.PositiveIntegerField(default=1)
    storage_location=models.CharField(max_length=120,blank=True)
    @property
    def is_expired(self): return date.today()>self.expiration_date
    @property
    def is_low_stock(self): return self.quantity<=self.minimum_quantity
    @property
    def is_expiring_soon(self): return not self.is_expired and date.today()>=self.expiration_date-timedelta(days=30)
    def __str__(self): return f"{self.item_name} / {self.lot_number}"
