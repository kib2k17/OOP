from django.urls import path
from . import views
urlpatterns=[path("",views.device_list,name="device-list"),path("new/",views.device_create,name="device-create")]
