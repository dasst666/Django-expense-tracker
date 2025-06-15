from django.urls import path 
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard_view"),
]
