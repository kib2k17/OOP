from django.urls import path
from . import views
urlpatterns=[
path("",views.competency_list,name="competency-list"),path("new/",views.competency_create,name="competency-create"),
path("test-methods/",views.testmethod_list,name="testmethod-list"),path("test-methods/new/",views.testmethod_create,name="testmethod-create")]
