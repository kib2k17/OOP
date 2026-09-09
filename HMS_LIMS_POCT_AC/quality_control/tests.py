from django.test import SimpleTestCase
from .models import QualityControlRecord
class QCTests(SimpleTestCase):
    def test_pass(self):
        q=QualityControlRecord(result=100,lower_limit=90,upper_limit=110)
        self.assertEqual(q.status,"PASS")
    def test_fail(self):
        q=QualityControlRecord(result=120,lower_limit=90,upper_limit=110)
        self.assertEqual(q.status,"FAIL")
