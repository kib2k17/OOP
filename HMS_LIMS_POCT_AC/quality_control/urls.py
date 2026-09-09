from django.urls import path
from . import views
urlpatterns=[path("",views.qc_list,name="qc-list"),path("new/",views.qc_create,name="qc-create")]
