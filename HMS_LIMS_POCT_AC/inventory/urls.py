from django.urls import path
from . import views
urlpatterns=[path("",views.inventory_list,name="inventory-list"),path("new/",views.inventory_create,name="inventory-create")]
