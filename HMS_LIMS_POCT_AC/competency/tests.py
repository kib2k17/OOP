from datetime import date,timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from operators.models import Department,Operator
from .models import Competency,TestMethod
class CompetencyTests(TestCase):
    def setUp(self):
        d=Department.objects.create(name="ICU"); self.o=Operator.objects.create(employee_id="E1",first_name="A",last_name="B",department=d)
        self.t=TestMethod.objects.create(name="Glucose"); self.u=User.objects.create_user(username="assessor",password="x")
    def test_expired(self):
        c=Competency(operator=self.o,test_method=self.t,assessor=self.u,completion_date=date.today()-timedelta(days=400),expiration_date=date.today()-timedelta(days=1))
        self.assertEqual(c.status,"EXPIRED")
    def test_due_soon(self):
        c=Competency(operator=self.o,test_method=self.t,assessor=self.u,completion_date=date.today()-timedelta(days=300),expiration_date=date.today()+timedelta(days=30))
        self.assertEqual(c.status,"DUE SOON")
