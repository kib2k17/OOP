from django.test import TestCase
from .models import Department, Operator
class OperatorModelTests(TestCase):
    def test_full_name(self):
        d=Department.objects.create(name="Emergency Department")
        o=Operator.objects.create(employee_id="E1",first_name="Jane",last_name="Smith",department=d)
        self.assertEqual(o.full_name,"Jane Smith")
