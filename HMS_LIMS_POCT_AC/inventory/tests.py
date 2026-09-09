from datetime import date,timedelta
from django.test import SimpleTestCase
from .models import InventoryItem
class InventoryTests(SimpleTestCase):
    def test_low_stock(self):
        i=InventoryItem(quantity=2,minimum_quantity=3,expiration_date=date.today()+timedelta(days=50))
        self.assertTrue(i.is_low_stock)
