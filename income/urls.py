from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path("", views.IncomeListView.as_view(), name="income_list"),
    path("add/", views.IncomeCreateView.as_view(), name="income_add"),
]
