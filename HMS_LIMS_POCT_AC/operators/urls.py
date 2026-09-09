from django.urls import path
from . import views
urlpatterns = [
    path("", views.operator_list, name="operator-list"),
    path("new/", views.operator_create, name="operator-create"),
    path("<int:pk>/", views.operator_detail, name="operator-detail"),
]
