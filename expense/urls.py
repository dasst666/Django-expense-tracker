from django.urls import path
from . import views

app_name = 'expense'

urlpatterns = [
    path("", views.ExpenseListView.as_view(), name="expense_list"),
    path("add/", views.ExpenseCreateView.as_view(), name="expense_add"),
]
